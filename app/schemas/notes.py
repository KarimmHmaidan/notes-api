from datetime import datetime

from pydantic import BaseModel,ConfigDict

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(NoteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: datetime

class MessageResponse(BaseModel):
    message: str


class PaginatedNotes(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[NoteResponse]