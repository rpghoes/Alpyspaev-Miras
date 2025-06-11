from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str
    content: str

class NoteOut(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True
