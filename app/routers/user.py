"""Rutas para la gestión de usuarios."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.database import async_session
from app.utils import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(tags=["Users"])


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """Obtiene un usuario por su email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


# --------------------------
# Registro de usuario
# --------------------------
@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(async_session)):
    """Registra a un usuario."""
    result = await get_user_by_email(user.email, db)
    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ya registrado"
        )
    new_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


# --------------------------
# Login / obtener JWT
# --------------------------
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(async_session),
):
    """Login de usuario y obtención de token JWT."""
    user = await get_user_by_email(form_data.username, db)
    if not user or not verify_password(form_data.password, user.password_hash):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    token = create_access_token({"id_usuario": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
