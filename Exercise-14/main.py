from fastapi import FastAPI
from config import get_settings

app = FastAPI()

settings = get_settings()

@app.get("/info")
def get_info():
    return {
        "debug": settings.DEBUG,
        "redis_host": settings.REDIS_HOST
    }
