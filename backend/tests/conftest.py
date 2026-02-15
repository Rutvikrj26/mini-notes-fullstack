"""Shared test fixtures."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.routes.notes import note_service_instance


@pytest.fixture(autouse=True)
def clear_notes() -> None:  # pyright: ignore[reportUnusedFunction]
    """Clear in-memory notes before each test."""
    note_service_instance.clear()


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """Async HTTP client for integration tests."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
