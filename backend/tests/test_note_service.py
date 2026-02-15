"""Unit tests for NoteService business logic."""

from app.models.note import NoteCreate
from app.services.note_service import NoteService


class TestNoteService:
    """Unit tests for NoteService."""

    def test_create_returns_note_with_id(self) -> None:
        """create() should return a NoteResponse with generated id."""
        service = NoteService()
        note = service.create(NoteCreate(title="Test", content="Body"))
        assert note.id
        assert note.title == "Test"
        assert note.content == "Body"
        assert note.created_at is not None

    def test_list_all_returns_empty_initially(self) -> None:
        """list_all() should return empty sequence on fresh service."""
        service = NoteService()
        assert list(service.list_all()) == []

    def test_list_all_returns_created_notes(self) -> None:
        """list_all() should return all created notes."""
        service = NoteService()
        service.create(NoteCreate(title="A", content="one"))
        service.create(NoteCreate(title="B", content="two"))
        assert len(service.list_all()) == 2

    def test_list_all_filters_by_title(self) -> None:
        """list_all(query=...) should filter by title."""
        service = NoteService()
        service.create(NoteCreate(title="Python Tips", content="body"))
        service.create(NoteCreate(title="Rust Tips", content="body"))
        results = service.list_all(query="python")
        assert len(results) == 1

    def test_list_all_filters_by_content(self) -> None:
        """list_all(query=...) should filter by content."""
        service = NoteService()
        service.create(NoteCreate(title="Guide", content="Learn Python"))
        service.create(NoteCreate(title="Guide", content="Learn Rust"))
        results = service.list_all(query="rust")
        assert len(results) == 1

    def test_list_all_case_insensitive(self) -> None:
        """Search should be case-insensitive."""
        service = NoteService()
        service.create(NoteCreate(title="PYTHON", content="body"))
        assert len(service.list_all(query="python")) == 1
        assert len(service.list_all(query="PYTHON")) == 1

    def test_clear_removes_all_notes(self) -> None:
        """clear() should remove all notes."""
        service = NoteService()
        service.create(NoteCreate(title="A", content="one"))
        service.clear()
        assert len(service.list_all()) == 0
