"""Pydantic models for the Note domain."""

from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a new note."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class NoteResponse(BaseModel):
    """Schema for note API responses."""

    id: str
    title: str
    content: str
    created_at: datetime
