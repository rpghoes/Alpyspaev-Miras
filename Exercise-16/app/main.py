from fastapi import FastAPI
from app.routers import note_routes
from app.models import Base
from app.database import engine

app = FastAPI(title="FastAPI + Alembic")

# Включаем маршруты
app.include_router(note_routes.router)

# Создаем таблицы при старте (необязательно, можно оставить миграции на Alembic)
@app.on_event("startup")
async def startup():
    # Удалите это, если используете alembic:
    # await conn.run_sync(Base.metadata.create_all)
    pass

