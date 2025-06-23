from fastapi import FastAPI
from app.routes import note_routes

app = FastAPI(
    title="Note API",
    description="js api for nts",
    version="1.0.0"
)

app.include_router(note_routes.router, prefix="/notes", tags=["Notes"])
