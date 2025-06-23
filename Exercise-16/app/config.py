from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:Kamilla27@localhost:5432/testdb"

    class Config:
        env_file = ".env"

settings = Settings()
