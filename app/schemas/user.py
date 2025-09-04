"""Esquemas para la genstión de tareas."""

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Esquema base de usuario."""

    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    """Esquema para crear un usuario."""

    password: str = Field(..., min_length=6)


class UserOut(UserBase):
    """Esquema para la salida de un usuario."""

    id: UUID
    created_at: datetime

    class Config:
        """Configuracion"""

        orm_mode = True
