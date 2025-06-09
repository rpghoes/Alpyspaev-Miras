from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from pydantic import BaseModel
from databases import Database

DATABASE_URL = "postgresql+asyncpg://username:Kamilla27!localhost:5432/dbname"  # поменяй на свои данные

# Pydantic-схемы
class NoteCreate(BaseModel):
    text: str

class NoteOut(BaseModel):
    id: int
    text: str
    created_at: datetime

# Модель и таблица
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

app = FastAPI()

# Асинхронная БД через databases
database = Database(DATABASE_URL)

# Синхронный движок для создания таблиц
engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), echo=True)

@app.on_event("startup")
async def on_startup():
    # Создаём таблицы, если их нет
    SQLModel.metadata.create_all(engine)
    await database.connect()

@app.on_event("shutdown")
async def on_shutdown():
    await database.disconnect()

@app.post("/notes", response_model=NoteOut)
async def create_note(note: NoteCreate):
    query = Note.__table__.insert().values(text=note.text, created_at=datetime.utcnow())
    note_id = await database.execute(query)
    # Получаем созданную заметку из БД
    query_select = Note.__table__.select().where(Note.id == note_id)
    created_note = await database.fetch_one(query_select)
    if not created_note:
        raise HTTPException(status_code=404, detail="Note not found after creation")
    return NoteOut(**created_note)

@app.get("/notes", response_model=List[NoteOut])
async def read_notes():
    query = Note.__table__.select()
    rows = await database.fetch_all(query)
    return [NoteOut(**row) for row in rows]
