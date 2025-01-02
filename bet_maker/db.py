"""
Модуль для инициализации соединения с базой данных PostgreSQL 
с использованием SQLAlchemy (асинхронный вариант).
"""
import os
import asyncio
from typing import NoReturn

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models import Base

POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "betsdb")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "betuser")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "betpassword")

DATABASE_URL: str = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

#: Асинхронный движок SQLAlchemy для подключения к БД
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

#: Фабрика для создания асинхронных сессий
SessionLocal: sessionmaker = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db() -> None:
    """
    Инициализирует базу данных, создавая необходимые таблицы (если они не существуют).
    Использует модель Base для отражения таблиц в БД.
    """
    async with engine.begin() as conn:
        # Создаём таблицы (если не существуют)
        await conn.run_sync(Base.metadata.create_all)
