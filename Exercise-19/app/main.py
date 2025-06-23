from fastapi import FastAPI
from app.routes import note_routes

app = FastAPI(
    title="Note API",
    description="API для управления заметками с улучшенной документацией",
    version="1.0.0"
)

app.include_router(note_routes.router, tags=["Notes"])
