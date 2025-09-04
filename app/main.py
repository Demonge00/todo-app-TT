from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import user, task

app = FastAPI(title="TODO API con FastAPI y PostgreSQL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
