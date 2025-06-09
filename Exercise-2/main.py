# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import User
from schemas import UserCreate, UserLogin, UserRead

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(username=user.username, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
