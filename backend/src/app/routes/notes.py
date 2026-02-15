"""API routes for notes CRUD operations."""

import logging
from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.models.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])

# Module-level singleton — shared across requests (in-memory storage)
note_service_instance = NoteService()


def get_note_service() -> NoteService:
    """Dependency that provides the NoteService singleton.

    Returns:
        The shared NoteService instance.
    """
    return note_service_instance


NoteServiceDep = Annotated[NoteService, Depends(get_note_service)]


@router.get("", response_model=list[NoteResponse])
async def list_notes(
    service: NoteServiceDep,
    q: str | None = Query(default=None, description="Search keyword for title/content"),
) -> Sequence[NoteResponse]:
    """List all notes, optionally filtered by a search keyword.

    Args:
        service: Injected NoteService instance.
        q: Optional case-insensitive search query.

    Returns:
        List of matching notes.
    """
    return service.list_all(query=q)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    data: NoteCreate,
    service: NoteServiceDep,
) -> NoteResponse:
    """Create a new note.

    Args:
        data: Note creation payload with title and content.
        service: Injected NoteService instance.

    Returns:
        The newly created note.
    """
    return service.create(data)
