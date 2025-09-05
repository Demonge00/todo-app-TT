"""Esquemas para la genstión de tareas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Esquema base de usuario."""

    email: EmailStr = Field(..., max_length=255)


class UserCreate(UserBase):
    """Esquema para crear un usuario."""

    password: str = Field(..., min_length=6)


class UserOut(UserBase):
    """Esquema para la salida de un usuario."""

    id: int
    fecha_creacion: datetime

    model_config = ConfigDict(from_attributes=True)
