"""Tests for the health endpoint."""

from httpx import AsyncClient


class TestHealth:
    """Health endpoint tests."""

    async def test_health_returns_ok(self, client: AsyncClient) -> None:
        """GET /health should return status ok."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
