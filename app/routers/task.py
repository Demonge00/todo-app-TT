"""Rutas para la gestión de tareas."""

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.database import async_session
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.models.task import Task
from app.models.user import User
from app.utils import get_current_user

router = APIRouter(tags=["tasks"])

# ---------- Operaciones de base de datos ----------


async def create_task(db: AsyncSession, task_in: TaskCreate, user: User) -> Task:
    """Crea una nueva tarea para el usuario dado."""
    task = Task(
        title=task_in.titulo,
        description=task_in.descripcion,
        estado=task_in.estado.value if task_in.estado is not None else None,
        id_usuario=user.id,
    )
    db.add(task)
    try:
        await db.commit()
        await db.refresh(task)
        return task
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"No se pudo crear la tarea: {str(e)}"
        ) from e


async def get_task_by_id(db: AsyncSession, task_id: UUID, user: User) -> Task | None:
    """Obtiene una tarea por su ID, asegurándose de que pertenezca al usuario."""
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.id_usuario == user.id)
    )
    return result.scalar_one_or_none()


async def update_task(db: AsyncSession, task: Task, task_in: TaskUpdate) -> Task:
    """Actualiza una tarea existente con los datos proporcionados."""
    if task_in.titulo is not None:
        task.titulo = task_in.titulo  # type: ignore
    if task_in.descripcion is not None:
        task.descripcion = task_in.descripcion  # type: ignore
    if task_in.estado is not None:
        task.estado = task_in.estado.value  # type: ignore
    try:
        await db.commit()
        await db.refresh(task)
        return task
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"No se pudo actualizar la tarea: {str(e)}"
        ) from e


async def delete_task(db: AsyncSession, task: Task) -> None:
    """Elimina una tarea existente."""
    try:
        await db.delete(task)
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=400, detail=f"No se pudo borrar la tarea: {str(e)}"
        ) from e


# ---------- Rutas ----------


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(
    task_in: TaskCreate,
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    """Endpoint para crear una tarea para usuarios autenticados."""
    return await create_task(db, task_in, current_user)


@router.get("/", response_model=list[TaskOut])
async def list_tasks_endpoint(
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    """Endpoint para listar todas las tareas del usuario autenticado."""
    result = await db.execute(select(Task).where(Task.id_usuario == current_user.id))
    return result.scalars().all()


@router.get("/{task_id}", response_model=TaskOut)
async def get_task_endpoint(
    task_id: UUID,
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    """Endpoint para obtener una tarea específica del usuario autenticado."""
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_task_endpoint(
    task_id: UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    """Endpoint para actualizar una tarea específica del usuario autenticado."""
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return await update_task(db, task, task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: UUID,
    db: AsyncSession = Depends(async_session),
    current_user: User = Depends(get_current_user),
):
    """Endpoint para borrar una tarea específica del usuario autenticado."""
    task = await get_task_by_id(db, task_id, current_user)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    await delete_task(db, task)
    return None
