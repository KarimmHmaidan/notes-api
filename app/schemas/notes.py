from pydantic import BaseModel,ConfigDict

class Note(BaseModel):
    title: str
    content: str

class NoteResponse(Note):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str