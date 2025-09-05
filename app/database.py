"""Configuración de la base de datos y sesión asíncrona"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://todo_user:todo_password@db:5432/todo_db",
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def async_session():
    """Proporciona una sesión asíncrona"""
    async with AsyncSessionLocal() as session:
        yield session
