from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.errors import ERROR_VALIDATION
from src.api.routes import router

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    yield


def _extract_validation_message(exc: RequestValidationError) -> str:
    """Extract a user-friendly message from validation errors."""
    errors = exc.errors()
    if not errors:
        return "Invalid request. Please check your input."
    first = errors[0]
    msg = first.get("msg", "")
    ctx = first.get("ctx") or {}
    # Pydantic model_validator ValueError: ctx may contain {"error": Exception}
    err_obj = ctx.get("error") if isinstance(ctx, dict) else None
    if err_obj is not None and hasattr(err_obj, "args") and err_obj.args:
        return str(err_obj.args[0])
    return msg or "Invalid request. Please provide a message or answer the pending question."


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cycle Trip Planner",
        description="AI-powered cycling trip planning agent",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        message = _extract_validation_message(exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": ERROR_VALIDATION, "message": message},
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)