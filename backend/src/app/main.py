"""FastAPI application factory with lifespan, CORS, and route registration."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.middleware.error_handler import register_error_handlers
from app.routes.notes import router as notes_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

settings = Settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — startup/shutdown logic."""
    logger.info("Starting %s", settings.app_name)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Build and configure the FastAPI application.

    Returns:
        Fully configured FastAPI app instance.
    """
    application = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS — allow Vite dev server
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handlers
    register_error_handlers(application)

    # Health endpoint
    @application.get("/health")
    async def health() -> dict[str, str]:  # pyright: ignore[reportUnusedFunction]
        """Health check endpoint."""
        return {"status": "ok"}

    # Routes
    application.include_router(notes_router)

    return application


app = create_app()
