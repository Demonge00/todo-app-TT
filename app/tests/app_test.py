"""Pytest"""

import pytest
import httpx
from app.main import app


@pytest.mark.asyncio
async def test_task_crud():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Registro
        response = await client.post(
            "/users/",
            json={"email": "testuser@example.com", "password": "testpassword"},
        )
        assert response.status_code == 200 or response.status_code == 400
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "email" in data
        else:
            assert response.json()["detail"] == "Email ya registrado"

        # Login
        response = await client.post(
            "/users/login/",
            data={"username": "testuser@example.com", "password": "testpassword"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Crear tarea
        response = await client.post(
            "/tasks/",
            json={"titulo": "Mi primera tarea", "descripcion": "Descripción inicial"},
            headers=headers,
        )
        assert response.status_code == 200 or response.status_code == 201
        task = response.json()
        assert task["titulo"] == "Mi primera tarea"
        task_id = task["id"]

        # 2. Listar tareas
        response = await client.get("/tasks/", headers=headers)
        assert response.status_code == 200
        tasks = response.json()
        assert any(t["id"] == task_id for t in tasks)

        # 3. Actualizar tarea
        response = await client.put(
            f"/tasks/{task_id}", json={"titulo": "Tarea actualizada"}, headers=headers
        )
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["titulo"] == "Tarea actualizada"

        # 4.Listar tarea específica
        response = await client.get(f"/tasks/{task_id}", headers=headers)
        assert response.status_code == 200
        specific_task = response.json()
        assert specific_task["id"] == task_id
        assert specific_task["titulo"] == "Tarea actualizada"

        # 5. Eliminar tarea
        response = await client.delete(f"/tasks/{task_id}", headers=headers)
        assert response.status_code == 204

        # 6. Confirmar que ya no está
        response = await client.get("/tasks/", headers=headers)
        tasks = response.json()
        assert not any(t["id"] == task_id for t in tasks)


@pytest.mark.asyncio
async def test_block_permission():
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 404

        # 1. Crear tarea
        response = await client.post(
            "/tasks/",
            json={"titulo": "Mi primera tarea", "descripcion": "Descripción inicial"},
        )
        assert response.status_code == 401

        # 2. Listar tareas
        response = await client.get("/tasks/")
        assert response.status_code == 401

        # 3. Actualizar tarea
        response = await client.put("/tasks/2", json={"titulo": "Tarea actualizada"})
        assert response.status_code == 401

        # 4.Listar tarea específica
        response = await client.get("/tasks/2")
        assert response.status_code == 401

        # 5. Eliminar tarea
        response = await client.delete("/tasks/2")
        assert response.status_code == 401
