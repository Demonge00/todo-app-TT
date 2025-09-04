"""Modelo de Usuario"""

from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    """Modelo de Usuario"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_creación = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
