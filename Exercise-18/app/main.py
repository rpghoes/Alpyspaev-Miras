from fastapi import FastAPI
from app.rate_limiter import RateLimiterMiddleware

app = FastAPI()

# ƒобавл€ем middleware дл€ ограничени€ частоты запросов
app.add_middleware(RateLimiterMiddleware, limit=5, window_seconds=60)

@app.get("/")
async def root():
    return {"message": "Rate limited endpoint"}
