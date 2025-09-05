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

## Instrucciones para correr el proyecto usando Docker (Recomendado)
### 1-Ejecutar el siguiente comando luego de clonar el repositorio:

```bash
docker compose up --build
```

***Las bases de datos migran automaticamente y las variables de entorno ya estan configuradas para que solo sea usar el comando y correr el proyecto***

---

## Instrucciones para correr el proyecto local
### 1-Crear un entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

***En caso de usar windows no usar source***

### 2-Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3-Configurar variables de estado

Ejemplo de `.env`

```env
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/db"
ALEMBIC_DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/db"
SECRET_KEY=8c47dc98274957f7954bb7ccd97b5fee
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4-Migrar a la base de datos

```bash
alembic upgrade head
```

---

### 5-Ejecutar la app

```bash
uvicorn app.main:app --reload --port 8000
```

---

## Uso de tests

### Local
```bash
pytest -q
```

---

### Docker
```bash
docker compose exec web pytest -q
```

## Endpoints principales y ejemplos de uso(curl)

### - `POST /users/` → registrar usuario 

```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass"}'
```

### Ejemplo de respuesta
{"email":"test@example.com","id":1,"fecha_creacion":"2025-09-05T20:33:47.632576Z"}

### - `POST /users/login/` → login (OAuth2 password/form)

```bash
curl -X POST http://localhost:8000/users/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass"
```

### Ejemplo de respuesta positiva
 {"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZF91c3","token_type":"bearer"}

### - `POST /tasks/` → crear tarea (Bearer token) 

```bash
TOKEN=eyJ... → Tomarlo de la respuesta anterior
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"titulo":"Comprar leche","descripcion":"Ir al supermercado"}'
```

### Ejemplo de respuesta positiva
{"titulo":"Comprar leche","descripcion":"Ir al supermercado","estado":"pendiente","id":"7afdfac0-3478-4404-9b5f-cbf285250d19","id_usuario":3,"fecha_creacion":"2025-09-05T20:40:57.734134Z"}

### - `GET /tasks/` → listar tareas del usuario autenticado

```bash
curl -X GET http://localhost:8000/tasks/ \
  -H "Authorization: Bearer $TOKEN"
```
### Ejemplo de respuesta positiva
{"titulo":"Comprar leche","descripcion":"Ir al supermercado","estado":"pendiente","id":"7afdfac0-3478-4404-9b5f-cbf285250d19","id_usuario":3,"fecha_creacion":"2025-09-05T20:40:57.734134Z"}

### - `GET /tasks/{id}` → detalle tarea 

```bash
curl -X GET http://localhost:8000/tasks/7afdfac0-3478-4404-9b5f-cbf285250d19 \
  -H "Authorization: Bearer $TOKEN"
```

### Ejemplo de respuesta positiva
{"titulo":"Comprar leche","descripcion":"Ir al supermercado","estado":"pendiente","id":"7afdfac0-3478-4404-9b5f-cbf285250d19","id_usuario":3,"fecha_creacion":"2025-09-05T20:40:57.734134Z"}

### - `PUT /tasks/{id}` → actualizar tarea

```bash
curl -X PUT http://localhost:8000/tasks/7afdfac0-3478-4404-9b5f-cbf285250d19 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"titulo":"Comprar manzanas","descripcion":"Ir al callejon"}'
```

### Ejemplo de respuesta positiva
{"titulo":"Comprar manzanas","descripcion":"Ir al callejon","estado":"pendiente","id":"7afdfac0-3478-4404-9b5f-cbf285250d19","id_usuario":3,"fecha_creacion":"2025-09-05T20:40:57.734134Z"}

### - `DELETE /tasks/{id}` → eliminar tarea  

```bash
curl -X DELETE http://localhost:8000/tasks/7afdfac0-3478-4404-9b5f-cbf285250d19 \
  -H "Authorization: Bearer $TOKEN"
```

### Ejemplo de respuesta positiva
Solo devuelve el estado 204

---

## Alembic(Solo si fuera necesario)
### Crear migracion
```bash
alembic revision --autogenerate -m "mensaje"
```
### Migrar
```bash
alembic upgrade head
```
