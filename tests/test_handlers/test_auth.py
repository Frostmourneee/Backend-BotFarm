import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_login_success(
        client,
        regular_user_create_data
):
    """
    Тест успешной авторизации
    """
    # Конвертируем UUID в строку для JSON
    user_data_for_api = {
        **regular_user_create_data,
        "project_id": str(regular_user_create_data["project_id"])
    }

    # Создаем пользователя через API
    response_create = await client.post(
        "/api/v1/users",
        json=user_data_for_api
    )
    assert response_create.status_code == status.HTTP_201_CREATED

    # Пытаемся авторизоваться
    response = await client.post(
        "/api/v1/login",
        data={
            "username": regular_user_create_data["login"],
            "password": regular_user_create_data["password"]
        }
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(
        client,
        regular_user_create_data
):
    """
    Тест авторизации с неправильным паролем
    """
    user_data_for_api = {
        **regular_user_create_data,
        "project_id": str(regular_user_create_data["project_id"])
    }

    response_create = await client.post(
        "/api/v1/users",
        json=user_data_for_api
    )
    assert response_create.status_code == status.HTTP_201_CREATED

    response = await client.post(
        "/api/v1/login",
        data={
            "username": regular_user_create_data["login"],
            "password": "wrong_password"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Неверный логин или пароль"


@pytest.mark.asyncio
async def test_login_user_not_found(
        client
):
    """
    Тест авторизации несуществующего пользователя
    """
    response = await client.post(
        "/api/v1/login",
        data={
            "username": "123@abc.com",
            "password": "password"
        }
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Неверный логин или пароль"


@pytest.mark.asyncio
async def test_login_canary_user_forbidden(
        client,
        user_create_data
):
    """
    Тест, что canary пользователь не может авторизоваться
    """
    user_data_for_api = {
        **user_create_data,
        "project_id": str(user_create_data["project_id"]),
        "domain": "canary"
    }

    response_create = await client.post(
        "/api/v1/users",
        json=user_data_for_api
    )
    assert response_create.status_code == status.HTTP_201_CREATED

    response = await client.post(
        "/api/v1/login",
        data={
            "username": user_data_for_api["login"],
            "password": user_data_for_api["password"]
        }
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Только реальные пользователи могут" in response.json()["detail"]
