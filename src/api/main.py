from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import router

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Cycle Trip Planner",
        description="AI-powered cycling trip planning agent",
        version="0.1.0",
        lifespan=lifespan,
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