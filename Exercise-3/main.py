# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, Session, select
from models import User
from schemas import UserCreate, UserLogin
from security import get_password_hash, verify_password

DATABASE_URL = "postgresql+asyncpg://user:mikocool17.@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)

app = FastAPI()

async def get_session() -> AsyncSession:
    async with Session(engine) as session:
        yield session

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

@app.post("/register")
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    hashed_pw = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    session.add(db_user)
    await session.commit()
    return {"msg": "User registered"}

@app.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful"}
