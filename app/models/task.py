"""Modelo de Tarea"""

import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class Task(Base):
    """Modelo de Tarea"""

    __tablename__ = "tasks"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    titulo = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    estado = Column(String, default="pendiente", nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    id_usuario = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")

    @validates("title")
    def validate_title(self, key, value):
        """Valida el título"""
        if not value or len(value) > 255:
            raise ValueError("El título debe tener entre 1 y 255 caracteres")
        return value

    @validates("description")
    def validate_description(self, key, value):
        """Valida la descripción para que no exceda los 5000 caracteres"""
        if value and len(value) > 5000:
            raise ValueError("Descripción demasiado larga")
        return value
