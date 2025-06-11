from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from models import Note, User
from schemas import NoteOut, NoteCreate, NoteUpdate
from auth import get_current_user, get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notes App with Auth, Pagination & Filtering")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Получить список заметок с пагинацией и фильтрацией
@app.get("/notes/", response_model=list[NoteOut])
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    search: str = Query("", min_length=0),
):
    query = db.query(Note).filter(Note.owner_id == current_user.id)
    if search:
        query = query.filter(
            Note.title.ilike(f"%{search}%") | Note.content.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

# ✅ Создать новую заметку
@app.post("/notes/", response_model=NoteOut)
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_note = Note(**note.dict(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# ✅ Получить одну заметку по id
@app.get("/notes/{note_id}", response_model=NoteOut)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# ✅ Обновить заметку
@app.put("/notes/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_data.title
    note.content = note_data.content
    db.commit()
    db.refresh(note)
    return note

# ✅ Удалить заметку
@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == current_user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"ok": True}
