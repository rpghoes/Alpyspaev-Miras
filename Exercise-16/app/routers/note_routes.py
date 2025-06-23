from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Note
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.get("/")
async def get_notes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note))
    return result.scalars().all()

@router.post("/")
async def create_note(title: str, content: str, db: AsyncSession = Depends(get_db)):
    note = Note(title=title, content=content)
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note
