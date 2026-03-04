from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import TypedDict

from src.agent.agent import agent
from src.tools.route import _route_geojson_store, _session_id_ctx

try:
    from pydantic_ai import AgentRunResultEvent, DeferredToolRequests, DeferredToolResults
    from pydantic_ai.messages import (
        ModelMessage,
        ModelRequest,
        ModelResponse,
        PartDeltaEvent,
        PartStartEvent,
        TextPart,
        TextPartDelta,
        ThinkingPart,
        ThinkingPartDelta,
        UserPromptPart,
        ToolCallPart,
    )
except ImportError:
    AgentRunResultEvent = object  # type: ignore[assignment,misc]
    DeferredToolRequests = object  # type: ignore[assignment,misc]
    DeferredToolResults = object  # type: ignore[assignment,misc]
    ModelMessage = object  # type: ignore[assignment,misc]
    ModelRequest = object  # type: ignore[assignment,misc]
    ModelResponse = object  # type: ignore[assignment,misc]
    PartDeltaEvent = object  # type: ignore[assignment,misc]
    PartStartEvent = object  # type: ignore[assignment,misc]
    TextPart = object  # type: ignore[assignment,misc]
    TextPartDelta = object  # type: ignore[assignment,misc]
    ThinkingPart = object  # type: ignore[assignment,misc]
    ThinkingPartDelta = object  # type: ignore[assignment,misc]
    UserPromptPart = object  # type: ignore[assignment,misc]
    ToolCallPart = object  # type: ignore[assignment,misc]

_sessions: dict[str, list] = {}


class _PendingDeferred(TypedDict):
    messages: list
    requests: "DeferredToolRequests"


_pending_deferred: dict[str, _PendingDeferred] = {}


def get_pending_tool_call_id(session_id: str) -> str | None:
    """If there is a pending ask_user question for this session, return its tool_call_id."""
    pending = _pending_deferred.get(session_id)
    if not pending:
        return None
    requests = pending["requests"]
    for call in requests.calls:
        if call.tool_name == "ask_user":
            return call.tool_call_id
    return None


def _extract_tools_used(messages: list) -> list[str]:
    """Extract unique tool names called in the given messages."""
    tools: list[str] = []
    for msg in messages:
        if isinstance(msg, ModelResponse):
            for part in msg.parts:
                if isinstance(part, ToolCallPart):
                    tools.append(part.tool_name)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for t in tools:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique


def _count_turns(messages: list) -> int:
    """Count the number of user turns in the full message history."""
    count = 0
    for msg in messages:
        if isinstance(msg, ModelRequest):
            for part in msg.parts:
                if isinstance(part, UserPromptPart):
                    count += 1
                    break
    return count


def run_turn(session_id: str, user_message: str) -> tuple[str | dict, list[str], int, dict | None]:
    """
    Run one turn of the conversation for a given session.

    Returns:
        (reply, tools_used, turn_count, route_geojson)
        When the agent defers with ask_user, reply is a dict with keys:
        question, options, tool_call_id (for CLI to display and await answer).
    """
    history = _sessions.get(session_id, [])
    prev_len = len(history)

    _pending_deferred.pop(session_id, None)

    # Set context so get_route can store GeoJSON for frontend (not sent to model)
    token = _session_id_ctx.set(session_id)
    try:
        result = agent.run_sync(user_message, message_history=history)
    finally:
        _session_id_ctx.reset(token)

    output = result.output
    all_messages = result.all_messages()

    if isinstance(output, DeferredToolRequests):
        requests = output
        for call in requests.calls:
            if call.tool_name == "ask_user":
                meta = requests.metadata.get(call.tool_call_id, {})
                question = meta.get("question", "")
                options = meta.get("options", [])
                _pending_deferred[session_id] = {
                    "messages": all_messages,
                    "requests": requests,
                }
                return (
                    {"question": question, "options": options, "tool_call_id": call.tool_call_id},
                    [],
                    _count_turns(all_messages),
                    None,
                )

    _sessions[session_id] = all_messages
    new_messages = all_messages[prev_len:]
    tools_used = _extract_tools_used(new_messages)
    route_geojson = _route_geojson_store.pop(session_id, None)
    turn_count = _count_turns(all_messages)

    return output, tools_used, turn_count, route_geojson


def run_turn_resume(
    session_id: str, tool_call_id: str, value: str
) -> tuple[str | dict, list[str], int, dict | None]:
    """
    Resume a deferred run with the user's answer to an ask_user question.

    Returns same shape as run_turn. May return another question dict if the agent
    defers again.
    """
    pending = _pending_deferred.pop(session_id, None)
    if not pending:
        raise ValueError("No pending question for this session. Send a new message instead.")

    messages = pending["messages"]
    requests = pending["requests"]

    results = DeferredToolResults()
    results.calls[tool_call_id] = value

    token = _session_id_ctx.set(session_id)
    prev_len = len(messages)
    try:
        result = agent.run_sync(
            message_history=messages,
            deferred_tool_results=results,
        )
    finally:
        _session_id_ctx.reset(token)

    output = result.output
    all_messages = result.all_messages()

    if isinstance(output, DeferredToolRequests):
        requests = output
        for call in requests.calls:
            if call.tool_name == "ask_user":
                meta = requests.metadata.get(call.tool_call_id, {})
                question = meta.get("question", "")
                options = meta.get("options", [])
                _pending_deferred[session_id] = {
                    "messages": all_messages,
                    "requests": requests,
                }
                return (
                    {"question": question, "options": options, "tool_call_id": call.tool_call_id},
                    [],
                    _count_turns(all_messages),
                    None,
                )

    _sessions[session_id] = all_messages
    new_messages = all_messages[prev_len:]
    tools_used = _extract_tools_used(new_messages)
    route_geojson = _route_geojson_store.pop(session_id, None)
    turn_count = _count_turns(all_messages)

    return output, tools_used, turn_count, route_geojson


async def run_turn_stream(
    session_id: str, user_message: str
) -> AsyncGenerator[dict, None]:
    """
    Run one turn of the conversation, streaming thinking and text deltas.
    Yields dicts: {"type": "thinking"|"text", "delta": str} or {"type": "done", ...}.
    """
    history = _sessions.get(session_id, [])
    prev_len = len(history)

    _pending_deferred.pop(session_id, None)

    token = _session_id_ctx.set(session_id)
    try:
        async for event in agent.run_stream_events(user_message, message_history=history):
            if isinstance(event, AgentRunResultEvent):
                result = event.result
                output = result.output
                all_messages = result.all_messages()

                if isinstance(output, DeferredToolRequests):
                    requests = output
                    for call in requests.calls:
                        if call.tool_name == "ask_user":
                            meta = requests.metadata.get(call.tool_call_id, {})
                            question = meta.get("question", "")
                            options = meta.get("options", [])
                            yield {
                                "type": "question",
                                "tool_call_id": call.tool_call_id,
                                "question": question,
                                "options": options,
                            }
                    _pending_deferred[session_id] = {
                        "messages": all_messages,
                        "requests": requests,
                    }
                    yield {
                        "type": "done",
                        "session_id": session_id,
                        "tools_used": [],
                        "turn_count": _count_turns(all_messages),
                        "waiting_for_input": True,
                    }
                    return

                _sessions[session_id] = all_messages
                new_messages = all_messages[prev_len:]
                tools_used = _extract_tools_used(new_messages)
                route_geojson = _route_geojson_store.pop(session_id, None)
                turn_count = _count_turns(all_messages)
                yield {
                    "type": "done",
                    "session_id": session_id,
                    "tools_used": tools_used,
                    "turn_count": turn_count,
                    "route_geojson": route_geojson,
                }
                return
            if isinstance(event, PartStartEvent):
                part = event.part
                if isinstance(part, ThinkingPart) and getattr(part, "content", None):
                    yield {"type": "thinking", "delta": part.content}
                elif isinstance(part, TextPart) and getattr(part, "content", None):
                    yield {"type": "text", "delta": part.content}
                elif isinstance(part, ToolCallPart) and part.tool_name != "ask_user":
                    yield {"type": "status", "message": f"Calling {part.tool_name}..."}
            elif isinstance(event, PartDeltaEvent):
                delta = event.delta
                if isinstance(delta, ThinkingPartDelta):
                    yield {"type": "thinking", "delta": getattr(delta, "content_delta", "") or ""}
                elif isinstance(delta, TextPartDelta):
                    yield {"type": "text", "delta": getattr(delta, "content_delta", "") or ""}
    finally:
        _session_id_ctx.reset(token)


async def run_turn_stream_resume(
    session_id: str, tool_call_id: str, value: str
) -> AsyncGenerator[dict, None]:
    """
    Resume a deferred run with the user's answer. Streams thinking and text as usual.
    """
    pending = _pending_deferred.pop(session_id, None)
    if not pending:
        yield {
            "type": "error",
            "message": "No pending question for this session. Send a new message instead.",
        }
        return

    messages = pending["messages"]
    requests = pending["requests"]

    results = DeferredToolResults()
    results.calls[tool_call_id] = value

    token = _session_id_ctx.set(session_id)
    prev_len = len(messages)
    try:
        async for event in agent.run_stream_events(
            message_history=messages,
            deferred_tool_results=results,
        ):
            if isinstance(event, AgentRunResultEvent):
                result = event.result
                output = result.output
                all_messages = result.all_messages()

                if isinstance(output, DeferredToolRequests):
                    requests = output
                    for call in requests.calls:
                        if call.tool_name == "ask_user":
                            meta = requests.metadata.get(call.tool_call_id, {})
                            question = meta.get("question", "")
                            options = meta.get("options", [])
                            yield {
                                "type": "question",
                                "tool_call_id": call.tool_call_id,
                                "question": question,
                                "options": options,
                            }
                    _pending_deferred[session_id] = {
                        "messages": all_messages,
                        "requests": requests,
                    }
                    yield {
                        "type": "done",
                        "session_id": session_id,
                        "tools_used": [],
                        "turn_count": _count_turns(all_messages),
                        "waiting_for_input": True,
                    }
                    return

                _sessions[session_id] = all_messages
                new_messages = all_messages[prev_len:]
                tools_used = _extract_tools_used(new_messages)
                route_geojson = _route_geojson_store.pop(session_id, None)
                turn_count = _count_turns(all_messages)
                yield {
                    "type": "done",
                    "session_id": session_id,
                    "tools_used": tools_used,
                    "turn_count": turn_count,
                    "route_geojson": route_geojson,
                }
                return
            if isinstance(event, PartStartEvent):
                part = event.part
                if isinstance(part, ThinkingPart) and getattr(part, "content", None):
                    yield {"type": "thinking", "delta": part.content}
                elif isinstance(part, TextPart) and getattr(part, "content", None):
                    yield {"type": "text", "delta": part.content}
                elif isinstance(part, ToolCallPart) and part.tool_name != "ask_user":
                    yield {"type": "status", "message": f"Calling {part.tool_name}..."}
            elif isinstance(event, PartDeltaEvent):
                delta = event.delta
                if isinstance(delta, ThinkingPartDelta):
                    yield {"type": "thinking", "delta": getattr(delta, "content_delta", "") or ""}
                elif isinstance(delta, TextPartDelta):
                    yield {"type": "text", "delta": getattr(delta, "content_delta", "") or ""}
    finally:
        _session_id_ctx.reset(token)


def clear_session(session_id: str) -> None:
    """Remove a session from the in-memory store."""
    _sessions.pop(session_id, None)
    _pending_deferred.pop(session_id, None)
