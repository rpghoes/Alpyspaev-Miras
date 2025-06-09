# migrate_passwords.py
from sqlmodel import Session, select
from models import User
from security import get_password_hash
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL)

async def migrate_passwords():
    async with Session(engine) as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        for user in users:
            if not user.hashed_password.startswith("$2b$"):  # простая проверка
                user.hashed_password = get_password_hash(user.hashed_password)
                session.add(user)
        await session.commit()
