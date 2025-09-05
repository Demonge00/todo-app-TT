# TODO API (FastAPI + PostgreSQL + Alembic)

API REST para administrar tareas (TODOs) con autenticación (JWT).  

## Requisitos

- Python 3.11+  
- Docker & Docker Compose  
- PostgreSQL (si corres sin Docker)  
- `git` (opcional)  

---

## Archivos importantes

- `app/` — código FastAPI (routers, modelos, schemas, utils, etc.)  
- `alembic/` — migraciones  
- `alembic.ini` — configuración Alembic  
- `Dockerfile`  
- `docker-compose.yml`  
- `requirements.txt`  
- `.env` (local)  

---

## Ejemplo de `.env`

```env
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/db"
ALEMBIC_DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/db"
SECRET_KEY=8c47dc98274957f7954bb7ccd97b5fee
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
En caso de usar docker***(Recomendado)*** sustituir localhost por db

---

## Instrucciones para correr el proyecto usando Docker
1-Ejecutar el siguiente comando luego de clonar el repositorio:
```
docker compose up --build
```
---


## Endpoints principales

- `POST /users/` → registrar usuario  
- `POST /users/login/` → login (OAuth2 password/form) → devuelve `access_token`  
- `POST /tasks/` → crear tarea (Bearer token)  
- `GET /tasks/` → listar tareas del usuario autenticado  
- `GET /tasks/{id}` → detalle tarea  
- `PUT /tasks/{id}` → actualizar tarea  
- `DELETE /tasks/{id}` → eliminar tarea  

---
