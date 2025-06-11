from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(NoteCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
