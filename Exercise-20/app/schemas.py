from pydantic import BaseModel, Field

class NoteSchema(BaseModel):
    title: str = Field(..., description="Заголовок заметки", example="Покупки")
    content: str = Field(..., description="Содержимое заметки", example="Купить хлеб и молоко")
