"""Esquemas para la genstión de tareas."""

from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


# Esto es para futura escalavilidad
class TaskStatus(str, Enum):
    """Enum para estados de la tarea."""

    PENDIENTE = "pendiente"
    COMPLETADA = "completada"


class TaskBase(BaseModel):
    """Esquema de tarea base."""

    titulo: str = Field(..., max_length=255)
    descripcion: Optional[str] = Field(None, max_length=5000)
    estado: Optional[TaskStatus] = TaskStatus.PENDIENTE


class TaskCreate(TaskBase):
    """Esquema para crear una tarea."""


class TaskUpdate(BaseModel):
    """Esquema para actualizar una tarea."""

    titulo: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = Field(None, max_length=5000)
    estado: Optional[TaskStatus] = None


class TaskOut(TaskBase):
    """Esquema para la salida de una tarea."""

    id: UUID
    id_usuario: UUID
    created_at: datetime

    class Config:
        """Configuracion"""

        orm_mode = True
