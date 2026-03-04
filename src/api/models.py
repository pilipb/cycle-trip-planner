from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class AnswerToQuestion(BaseModel):
    tool_call_id: str
    value: str


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(default="", max_length=4000)
    answer_to_question: AnswerToQuestion | None = None

    @model_validator(mode="after")
    def require_message_or_answer(self) -> "ChatRequest":
        if self.answer_to_question is not None:
            return self
        if not (self.message or "").strip():
            raise ValueError("Either message or answer_to_question must be provided")
        return self


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    tools_used: list[str] = []
    turn_count: int
    route_geojson: dict | None = None  # GeoJSON FeatureCollection for map display when route was fetched
