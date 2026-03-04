from __future__ import annotations

import json
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def _parse_sse_events(content: bytes) -> list[dict]:
    """Parse SSE stream into list of data payloads."""
    events = []
    for block in content.decode().strip().split("\n\n"):
        if not block:
            continue
        for line in block.split("\n"):
            if line.startswith("data: "):
                raw = line[6:]
                if raw and raw != "[DONE]":
                    try:
                        events.append(json.loads(raw))
                    except json.JSONDecodeError:
                        pass
                break
    return events


async def _mock_run_turn_stream(session_id: str, message: str):
    yield {"type": "text", "delta": "Here is your cycling itinerary."}
    yield {
        "type": "done",
        "session_id": session_id,
        "tools_used": [],
        "turn_count": 1,
        "route_geojson": None,
    }


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_creates_session_id_when_none_provided():
    with patch("src.api.routes.run_turn_stream", side_effect=_mock_run_turn_stream):
        response = client.post("/api/v1/chat", json={"message": "Plan a Berlin to Prague trip"})
    assert response.status_code == 200
    events = _parse_sse_events(response.content)
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) == 1
    assert "session_id" in done_events[0]
    assert done_events[0]["session_id"]


def test_chat_preserves_provided_session_id():
    sid = "my-test-session-123"

    async def mock_stream(session_id: str, message: str):
        yield {"type": "text", "delta": "OK"}
        yield {
            "type": "done",
            "session_id": session_id,
            "tools_used": [],
            "turn_count": 1,
            "route_geojson": None,
        }

    with patch("src.api.routes.run_turn_stream", side_effect=mock_stream):
        response = client.post(
            "/api/v1/chat",
            json={"session_id": sid, "message": "Plan a trip"},
        )
    assert response.status_code == 200
    events = _parse_sse_events(response.content)
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) == 1
    assert done_events[0]["session_id"] == sid


def test_chat_streams_text_then_done():
    async def mock_stream(session_id: str, message: str):
        yield {"type": "text", "delta": "Great cycling plan!"}
        yield {
            "type": "done",
            "session_id": session_id,
            "tools_used": [],
            "turn_count": 1,
            "route_geojson": None,
        }

    with patch("src.api.routes.run_turn_stream", side_effect=mock_stream):
        response = client.post("/api/v1/chat", json={"message": "Plan a trip"})
    assert response.status_code == 200
    events = _parse_sse_events(response.content)
    text_events = [e for e in events if e.get("type") == "text"]
    assert any(e.get("delta") == "Great cycling plan!" for e in text_events)
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) == 1


def test_chat_done_event_contains_tools_used_and_turn_count():
    tools = ["get_route", "get_weather", "find_accommodation"]

    async def mock_stream(session_id: str, message: str):
        yield {"type": "text", "delta": "Hi"}
        yield {
            "type": "done",
            "session_id": session_id,
            "tools_used": tools,
            "turn_count": 3,
            "route_geojson": None,
        }

    with patch("src.api.routes.run_turn_stream", side_effect=mock_stream):
        response = client.post("/api/v1/chat", json={"message": "Plan a trip"})
    assert response.status_code == 200
    events = _parse_sse_events(response.content)
    done_events = [e for e in events if e.get("type") == "done"]
    assert len(done_events) == 1
    assert done_events[0]["tools_used"] == tools
    assert done_events[0]["turn_count"] == 3


def test_chat_rejects_empty_message():
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_rejects_missing_message():
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_rejects_message_too_long():
    response = client.post("/api/v1/chat", json={"message": "x" * 4001})
    assert response.status_code == 422


def test_chat_sse_format():
    with patch("src.api.routes.run_turn_stream", side_effect=_mock_run_turn_stream):
        response = client.post("/api/v1/chat", json={"message": "Test"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    events = _parse_sse_events(response.content)
    assert len(events) >= 2
    assert events[0]["type"] == "text"
    assert "delta" in events[0]
    done = events[-1]
    assert done["type"] == "done"
    assert set(done.keys()) >= {"session_id", "tools_used", "turn_count", "route_geojson"}
    assert isinstance(done["tools_used"], list)
    assert isinstance(done["turn_count"], int)
