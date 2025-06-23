from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, CI/CD!", "debug": settings.DEBUG}
