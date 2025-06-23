from pydantic import BaseModel, Field

class NoteBase(BaseModel):
    title: str = Field(..., description="Заголовок заметки", example="Список покупок")
    content: str = Field(..., description="Содержимое заметки", example="Молоко, хлеб, сыр")

class NoteCreate(NoteBase):
    pass

class NoteOut(NoteBase):
    id: int = Field(..., description="Уникальный идентификатор заметки", example=1)

    class Config:
        orm_mode = True
