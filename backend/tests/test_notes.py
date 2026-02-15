"""Tests for the notes API endpoints."""

from httpx import AsyncClient


class TestCreateNote:
    """POST /notes tests."""

    async def test_create_note_returns_201(self, client: AsyncClient) -> None:
        """Creating a note should return 201 with id and created_at."""
        payload = {"title": "Test Note", "content": "Hello world"}
        response = await client.post("/notes", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Note"
        assert data["content"] == "Hello world"
        assert "id" in data
        assert "created_at" in data

    async def test_create_note_missing_title_returns_422(self, client: AsyncClient) -> None:
        """Missing title should return 422 validation error."""
        response = await client.post("/notes", json={"content": "no title"})
        assert response.status_code == 422

    async def test_create_note_missing_content_returns_422(self, client: AsyncClient) -> None:
        """Missing content should return 422 validation error."""
        response = await client.post("/notes", json={"title": "no content"})
        assert response.status_code == 422

    async def test_create_note_empty_title_returns_422(self, client: AsyncClient) -> None:
        """Empty string title should return 422 validation error."""
        response = await client.post("/notes", json={"title": "", "content": "body"})
        assert response.status_code == 422

    async def test_create_note_empty_body_returns_422(self, client: AsyncClient) -> None:
        """Empty request body should return 422 validation error."""
        response = await client.post("/notes", json={})
        assert response.status_code == 422


class TestListNotes:
    """GET /notes tests."""

    async def test_list_notes_empty(self, client: AsyncClient) -> None:
        """Should return empty array when no notes exist."""
        response = await client.get("/notes")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_notes_returns_created(self, client: AsyncClient) -> None:
        """Should return notes after creation."""
        await client.post("/notes", json={"title": "Note 1", "content": "Content 1"})
        await client.post("/notes", json={"title": "Note 2", "content": "Content 2"})
        response = await client.get("/notes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    async def test_search_notes_by_title(self, client: AsyncClient) -> None:
        """Search by q param should filter notes by title."""
        await client.post("/notes", json={"title": "Python Guide", "content": "Learn Python"})
        await client.post("/notes", json={"title": "Rust Guide", "content": "Learn Rust"})
        response = await client.get("/notes", params={"q": "python"})
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert "python" in results[0]["title"].lower()

    async def test_search_notes_by_content(self, client: AsyncClient) -> None:
        """Search by q param should also match content."""
        await client.post("/notes", json={"title": "Guide", "content": "Learn Python basics"})
        await client.post("/notes", json={"title": "Guide", "content": "Learn Rust basics"})
        response = await client.get("/notes", params={"q": "rust"})
        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert "rust" in results[0]["content"].lower()

    async def test_search_notes_case_insensitive(self, client: AsyncClient) -> None:
        """Search should be case-insensitive."""
        await client.post("/notes", json={"title": "PYTHON", "content": "content"})
        response = await client.get("/notes", params={"q": "python"})
        assert response.status_code == 200
        assert len(response.json()) == 1

    async def test_search_notes_no_match(self, client: AsyncClient) -> None:
        """Search with no matches should return empty array."""
        await client.post("/notes", json={"title": "Hello", "content": "World"})
        response = await client.get("/notes", params={"q": "xyz"})
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_notes_without_query_returns_all(self, client: AsyncClient) -> None:
        """GET /notes without q should return all notes."""
        await client.post("/notes", json={"title": "A", "content": "one"})
        await client.post("/notes", json={"title": "B", "content": "two"})
        response = await client.get("/notes")
        assert response.status_code == 200
        assert len(response.json()) == 2
