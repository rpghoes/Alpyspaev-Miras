from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class NoteOut(NoteBase):
    id: int
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        orm_mode = True
