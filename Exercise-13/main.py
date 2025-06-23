from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Note
from cache import get_cached_notes, set_cached_notes, invalidate_cache

app = FastAPI()

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Эндпоинт: получить список заметок с кешем Redis
@app.get("/notes")
async def read_notes(db: Session = Depends(get_db)):
    cached = await get_cached_notes()
    if cached:
        return {"source": "cache", "data": cached}

    notes = db.query(Note).all()
    data = [{"id": n.id, "title": n.title, "content": n.content} for n in notes]
    await set_cached_notes(data)
    return {"source": "db", "data": data}

# Эндпоинт: создать новую заметку и сбросить кеш
@app.post("/notes")
async def create_note(title: str, content: str, db: Session = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    db.commit()
    await invalidate_cache()
    return {"message": "Note created"}

# Эндпоинт: удалить заметку и сбросить кеш
@app.delete("/notes/{note_id}")
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    await invalidate_cache()
    return {"message": "Note deleted"}
