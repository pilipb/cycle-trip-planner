from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.agent.session import (
    _pending_deferred,
    _sessions,
    clear_session,
    get_pending_tool_call_id,
    run_turn,
    run_turn_resume,
    run_turn_stream,
)


def _make_mock_result(reply: str = "Here is your cycling plan.", messages: list | None = None):
    mock = MagicMock()
    mock.output = reply
    mock.all_messages.return_value = messages or []
    return mock


def test_run_turn_returns_reply():
    mock_result = _make_mock_result("Test reply")
    with patch("src.agent.session.agent.run_sync", return_value=mock_result):
        reply, tools_used, turn_count, _ = run_turn("session-001", "Plan a trip from Berlin to Prague")
    assert reply == "Test reply"


def test_run_turn_returns_empty_tools_when_no_tool_messages():
    mock_result = _make_mock_result(messages=[])
    with patch("src.agent.session.agent.run_sync", return_value=mock_result):
        _, tools_used, _, _ = run_turn("session-002", "Hello")
    assert tools_used == []


def test_run_turn_stores_session():
    _sessions.clear()
    mock_result = _make_mock_result(messages=["msg1", "msg2"])
    with patch("src.agent.session.agent.run_sync", return_value=mock_result):
        run_turn("session-abc", "Plan a trip")
    assert "session-abc" in _sessions
    assert _sessions["session-abc"] == ["msg1", "msg2"]


def test_run_turn_passes_history_to_agent():
    _sessions.clear()
    first_messages = [MagicMock()]
    _sessions["session-hist"] = first_messages

    mock_result = _make_mock_result()
    with patch("src.agent.session.agent.run_sync", return_value=mock_result) as mock_run:
        run_turn("session-hist", "Follow-up message")

    mock_run.assert_called_once_with("Follow-up message", message_history=first_messages)


def test_run_turn_different_sessions_are_independent():
    _sessions.clear()
    msgs_a = [MagicMock()]
    msgs_b = [MagicMock(), MagicMock()]

    mock_a = _make_mock_result("Reply A", messages=msgs_a)
    mock_b = _make_mock_result("Reply B", messages=msgs_b)

    with patch("src.agent.session.agent.run_sync", side_effect=[mock_a, mock_b]):
        reply_a, _, _, _ = run_turn("session-A", "Message A")
        reply_b, _, _, _ = run_turn("session-B", "Message B")

    assert reply_a == "Reply A"
    assert reply_b == "Reply B"
    assert _sessions["session-A"] == msgs_a
    assert _sessions["session-B"] == msgs_b


def test_clear_session_removes_session():
    _sessions["to-delete"] = ["some", "messages"]
    clear_session("to-delete")
    assert "to-delete" not in _sessions


def test_clear_nonexistent_session_does_not_raise():
    clear_session("nonexistent-session-xyz")  # Should not raise


@pytest.mark.asyncio
async def test_run_turn_stream_yields_events_then_done():
    from pydantic_ai import AgentRunResultEvent
    from pydantic_ai.messages import PartDeltaEvent, TextPartDelta
    from pydantic_ai.run import AgentRunResult

    async def mock_run_stream_events(message, *, message_history=None):
        yield PartDeltaEvent(index=0, delta=TextPartDelta(content_delta="Hello "))
        yield PartDeltaEvent(index=0, delta=TextPartDelta(content_delta="world."))
        mock_result = MagicMock(spec=AgentRunResult)
        mock_result.output = "Hello world."
        mock_result.all_messages.return_value = []
        yield AgentRunResultEvent(result=mock_result)

    with patch("src.agent.session.agent.run_stream_events", side_effect=mock_run_stream_events):
        events = []
        async for chunk in run_turn_stream("stream-session", "Hi"):
            events.append(chunk)
    text_deltas = [e for e in events if e.get("type") == "text"]
    assert len(text_deltas) == 2
    assert text_deltas[0]["delta"] == "Hello "
    assert text_deltas[1]["delta"] == "world."
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) == 1
    assert done_events[0]["session_id"] == "stream-session"
    assert done_events[0]["tools_used"] == []
    assert done_events[0]["turn_count"] == 0
    assert "route_geojson" in done_events[0]


def test_run_turn_returns_question_dict_when_deferred():
    from pydantic_ai.output import DeferredToolRequests
    from pydantic_ai.messages import ToolCallPart

    _sessions.clear()
    _pending_deferred.clear()

    call = ToolCallPart(tool_name="ask_user", args={}, tool_call_id="tc-123")
    deferred = DeferredToolRequests(
        calls=[call],
        approvals=[],
        metadata={"tc-123": {"question": "How far per day?", "options": ["50 km", "100 km"]}},
    )
    mock_result = MagicMock()
    mock_result.output = deferred
    mock_result.all_messages.return_value = [MagicMock()]

    with patch("src.agent.session.agent.run_sync", return_value=mock_result):
        reply, tools_used, turn_count, _ = run_turn("defer-session", "Plan London to Edinburgh")

    assert isinstance(reply, dict)
    assert reply["question"] == "How far per day?"
    assert reply["options"] == ["50 km", "100 km"]
    assert reply["tool_call_id"] == "tc-123"
    assert tools_used == []
    assert get_pending_tool_call_id("defer-session") == "tc-123"


def test_run_turn_resume_continues_after_answer():
    _sessions.clear()
    _pending_deferred.clear()

    mock_result = MagicMock()
    mock_result.output = "Here is your 5-day plan."
    mock_result.all_messages.return_value = [MagicMock(), MagicMock()]

    # Simulate pending state from a previous deferred run
    from pydantic_ai.output import DeferredToolRequests
    from pydantic_ai.messages import ToolCallPart

    call = ToolCallPart(tool_name="ask_user", args={}, tool_call_id="tc-456")
    _pending_deferred["resume-session"] = {
        "messages": [MagicMock()],
        "requests": DeferredToolRequests(calls=[call], approvals=[], metadata={}),
    }

    with patch("src.agent.session.agent.run_sync", return_value=mock_result) as mock_run:
        reply, tools_used, _, _ = run_turn_resume("resume-session", "tc-456", "100 km")

    assert reply == "Here is your 5-day plan."
    mock_run.assert_called_once()
    call_kw = mock_run.call_args.kwargs
    assert "message_history" in call_kw
    assert "deferred_tool_results" in call_kw
    assert call_kw["deferred_tool_results"].calls["tc-456"] == "100 km"
