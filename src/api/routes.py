from __future__ import annotations

import uuid

from fastapi import APIRouter

from src.agent.session import run_turn
from src.api.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1")


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return the agent's response."""
    session_id = request.session_id or str(uuid.uuid4())
    reply, tools_used, turn_count, route_geojson = run_turn(session_id, request.message)
    return ChatResponse(
        session_id=session_id,
        reply=reply,
        tools_used=tools_used,
        turn_count=turn_count,
        route_geojson=route_geojson,
    )
