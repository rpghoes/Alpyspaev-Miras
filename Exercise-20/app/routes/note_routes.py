from fastapi import APIRouter, HTTPException, Body
from app.models import Note, NoteCreate, NoteUpdate

router = APIRouter()

# Temporary storage
fake_db: list[Note] = []
next_id = 1

@router.get("/", summary="Get list of notes")
def get_notes():
    return fake_db

@router.post("/", summary="Create a new note", response_model=Note)
def create_note(note: NoteCreate = Body(...)):
    global next_id
    new_note = Note(id=next_id, **note.dict())
    fake_db.append(new_note)
    next_id += 1
    return new_note

@router.get("/{note_id}", summary="Get a note by ID", response_model=Note)
def get_note(note_id: int):
    for note in fake_db:
        if note.id == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@router.put("/{note_id}", summary="Update a note", response_model=Note)
def update_note(note_id: int, note_update: NoteUpdate = Body(...)):
    for note in fake_db:
        if note.id == note_id:
            if note_update.title is not None:
                note.title = note_update.title
            if note_update.content is not None:
                note.content = note_update.content
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@router.delete("/{note_id}", summary="Delete a note")
def delete_note(note_id: int):
    for i, note in enumerate(fake_db):
        if note.id == note_id:
            del fake_db[i]
            return {"ok": True}
    raise HTTPException(status_code=404, detail="Note not found")
