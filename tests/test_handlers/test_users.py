import uuid

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_user_success(
        client,
        user_create_data
):
    """
    Тест успешного создания пользователя
    """
    user_data_for_api = {
        **user_create_data,
        "project_id": str(user_create_data["project_id"])
    }

    response = await client.post(
        "/api/v1/users",
        json=user_data_for_api
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_user_duplicate(
        client,
        user_create_data
):
    """
    Тест создания пользователя с существующим логином
    """
    user_data_for_api = {
        **user_create_data,
        "project_id": str(user_create_data["project_id"])
    }

    response1 = await client.post("/api/v1/users", json=user_data_for_api)
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = await client.post("/api/v1/users", json=user_data_for_api)
    assert response2.status_code == status.HTTP_409_CONFLICT
    assert response2.json()["detail"] == "Пользователь уже есть в БД"


@pytest.mark.asyncio
async def test_get_users_unauthorized(client):
    """
    Тест, что без авторизации нельзя получить пользователей
    """
    response = await client.get("/api/v1/users")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_acquire_lock_user_not_found(
        client,
        auth_headers
):
    """
    Тест блокировки несуществующего пользователя
    """
    non_existent_id = uuid.uuid4()
    response = await client.post(
        f"/api/v1/users/{non_existent_id}/lock",
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
