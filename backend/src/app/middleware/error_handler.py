"""Error handler middleware for consistent JSON error responses."""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, *, code: str, status_code: int = 500) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    """Resource not found."""

    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(
            message=f"{resource} '{resource_id}' not found",
            code="NOT_FOUND",
            status_code=404,
        )


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI app.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(AppError)
    async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:  # pyright: ignore[reportUnusedFunction]
        """Handle known application errors with structured JSON."""
        logger.warning("AppError: %s (code=%s, status=%d)", exc.message, exc.code, exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_request: Request, exc: Exception) -> JSONResponse:  # pyright: ignore[reportUnusedFunction]
        """Handle unexpected errors with a safe generic message."""
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                }
            },
        )
