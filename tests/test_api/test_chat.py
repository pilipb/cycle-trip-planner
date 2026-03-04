from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def _mock_run_turn(reply="Here is your cycling itinerary.", tools=None, turns=1, route_geojson=None):
    return (reply, tools or [], turns, route_geojson)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_creates_session_id_when_none_provided():
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn()):
        response = client.post("/api/v1/chat", json={"message": "Plan a Berlin to Prague trip"})
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["session_id"]  # Non-empty UUID string


def test_chat_preserves_provided_session_id():
    sid = "my-test-session-123"
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn()) as mock_rt:
        response = client.post(
            "/api/v1/chat",
            json={"session_id": sid, "message": "Plan a trip"},
        )
    assert response.status_code == 200
    assert response.json()["session_id"] == sid
    mock_rt.assert_called_once_with(sid, "Plan a trip")


def test_chat_returns_reply():
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn("Great cycling plan!")):
        response = client.post("/api/v1/chat", json={"message": "Plan a trip"})
    assert response.json()["reply"] == "Great cycling plan!"


def test_chat_returns_tools_used():
    tools = ["get_route", "get_weather", "find_accommodation"]
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn(tools=tools)):
        response = client.post("/api/v1/chat", json={"message": "Plan a trip"})
    assert response.json()["tools_used"] == tools


def test_chat_returns_turn_count():
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn(turns=3)):
        response = client.post("/api/v1/chat", json={"message": "Plan a trip"})
    assert response.json()["turn_count"] == 3


def test_chat_rejects_empty_message():
    response = client.post("/api/v1/chat", json={"message": ""})
    assert response.status_code == 422


def test_chat_rejects_missing_message():
    response = client.post("/api/v1/chat", json={})
    assert response.status_code == 422


def test_chat_rejects_message_too_long():
    response = client.post("/api/v1/chat", json={"message": "x" * 4001})
    assert response.status_code == 422


def test_chat_response_schema():
    with patch("src.api.routes.run_turn", return_value=_mock_run_turn()):
        response = client.post("/api/v1/chat", json={"message": "Test"})
    data = response.json()
    assert set(data.keys()) >= {"session_id", "reply", "tools_used", "turn_count", "route_geojson"}
    assert isinstance(data["tools_used"], list)
    assert isinstance(data["turn_count"], int)
