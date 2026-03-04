from __future__ import annotations

from src.agent.agent import agent

try:
    from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse
    from pydantic_ai.messages import UserPromptPart, ToolCallPart
except ImportError:
    # Fallback for older pydantic-ai versions
    ModelMessage = object  # type: ignore[assignment,misc]
    ModelRequest = object  # type: ignore[assignment,misc]
    ModelResponse = object  # type: ignore[assignment,misc]
    UserPromptPart = object  # type: ignore[assignment,misc]
    ToolCallPart = object  # type: ignore[assignment,misc]

_sessions: dict[str, list] = {}


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


def run_turn(session_id: str, user_message: str) -> tuple[str, list[str], int]:
    """
    Run one turn of the conversation for a given session.

    Returns:
        (reply, tools_used, turn_count)
    """
    history = _sessions.get(session_id, [])
    prev_len = len(history)

    result = agent.run_sync(user_message, message_history=history)

    all_messages = result.all_messages()
    _sessions[session_id] = all_messages

    # Tools used only in this turn
    new_messages = all_messages[prev_len:]
    tools_used = _extract_tools_used(new_messages)

    turn_count = _count_turns(all_messages)

    return result.output, tools_used, turn_count


def clear_session(session_id: str) -> None:
    """Remove a session from the in-memory store."""
    _sessions.pop(session_id, None)
