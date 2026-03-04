from __future__ import annotations

import json
import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from src.agent.session import get_pending_tool_call_id, run_turn_stream, run_turn_stream_resume
from src.api.errors import error_payload, normalize_exception
from src.api.models import ChatRequest

router = APIRouter(prefix="/api/v1")


async def _stream_chat_events(session_id: str, message: str):
    """Async generator that yields SSE data lines."""
    try:
        async for chunk in run_turn_stream(session_id, message):
            yield f"data: {json.dumps(chunk)}\n\n"
    except Exception as e:
        message, code = normalize_exception(e)
        yield f"data: {json.dumps(error_payload(message, code))}\n\n"
        raise


async def _stream_chat_events_resume(session_id: str, tool_call_id: str, value: str):
    """Async generator that yields SSE data lines when resuming after a question."""
    try:
        async for chunk in run_turn_stream_resume(session_id, tool_call_id, value):
            yield f"data: {json.dumps(chunk)}\n\n"
    except Exception as e:
        message, code = normalize_exception(e)
        yield f"data: {json.dumps(error_payload(message, code))}\n\n"
        raise


@router.post("/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    """Stream the agent's thinking and response as Server-Sent Events."""
    session_id = request.session_id or str(uuid.uuid4())
    if request.answer_to_question is not None:
        stream = _stream_chat_events_resume(
            session_id,
            request.answer_to_question.tool_call_id,
            request.answer_to_question.value,
        )
    else:
        pending_id = get_pending_tool_call_id(session_id)
        if pending_id is not None:
            stream = _stream_chat_events_resume(
                session_id,
                pending_id,
                request.message.strip(),
            )
        else:
            stream = _stream_chat_events(session_id, request.message)
    return StreamingResponse(
        stream,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
