"""In-memory note storage and business logic."""

import logging
from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

from app.models.note import NoteCreate, NoteResponse

logger = logging.getLogger(__name__)


class NoteService:
    """Service layer for note CRUD operations with in-memory storage."""

    def __init__(self) -> None:
        self._notes: list[NoteResponse] = []

    def create(self, data: NoteCreate) -> NoteResponse:
        """Create a new note and return it.

        Args:
            data: Validated note creation payload.

        Returns:
            The newly created note with generated id and timestamp.
        """
        note = NoteResponse(
            id=str(uuid4()),
            title=data.title,
            content=data.content,
            created_at=datetime.now(UTC),
        )
        self._notes.append(note)
        logger.info("Created note %s with title '%s'", note.id, note.title)
        return note

    def list_all(self, query: str | None = None) -> Sequence[NoteResponse]:
        """Return all notes, optionally filtered by keyword.

        Args:
            query: Case-insensitive search term applied to title and content.

        Returns:
            Sequence of matching notes.
        """
        if query is None:
            logger.info("Listing all notes (count=%d)", len(self._notes))
            return list(self._notes)

        q_lower = query.lower()
        results = [
            note
            for note in self._notes
            if q_lower in note.title.lower() or q_lower in note.content.lower()
        ]
        logger.info("Searched notes for '%s' — %d result(s)", query, len(results))
        return results

    def clear(self) -> None:
        """Remove all notes (used in testing)."""
        self._notes.clear()
