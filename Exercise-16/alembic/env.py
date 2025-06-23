from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.models import Base  # Импортируй Base из своего проекта
from app.config import settings  # Подключи настройки подключения

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_migrations():
        async with connectable.begin() as conn:
            await conn.run_sync(context.run_migrations)

    import asyncio
    asyncio.run(run_migrations())

run_migrations_online()
    