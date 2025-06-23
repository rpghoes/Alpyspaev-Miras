from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SECRET_KEY: str = "supersecret"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
