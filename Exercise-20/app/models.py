from pydantic import BaseModel, Field

class Note(BaseModel):
    id: int
    title: str
    content: str

class NoteCreate(BaseModel):
    title: str = Field(..., example="My note")
    content: str = Field(..., example="Note content")

class NoteUpdate(BaseModel):
    title: str | None = Field(None, example="New title")
    content: str | None = Field(None, example="New content")
