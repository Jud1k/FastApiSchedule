import pytest
from httpx import AsyncClient

from app.domain.auth.schemas import UserRegister
from tests.factories import UserFactory
from tests.utils import generate_invalid_token, generate_expired_token


@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    user_in = UserRegister(email="example@mail.com", password="password123")
    user_in_data = user_in.model_dump()

    response = await client.post("/api/v1/register/", json=user_in_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["email"] == user_in_data["email"]


@pytest.mark.asyncio
async def test_register_and_login_flow(client: AsyncClient):
    user_register = UserRegister(email="example@mail.com", password="password123")
    user_register_data = user_register.model_dump()

    register_response = await client.post("/api/v1/register/", json=user_register_data)
    assert register_response.status_code == 201
    response_data = register_response.json()
    assert response_data["email"] == user_register_data["email"]

    user_login_data = {
        "username": user_register.email,
        "password": user_register.password,
        "grant_type": "password",
    }
    login_response = await client.post("/api/v1/login/", data=user_login_data)
    assert login_response.status_code == 200
    login_response_data = login_response.json()
    assert "access_token" in login_response_data
    assert "refresh_token" in login_response_data
    assert login_response_data["user"]["email"] == user_register.email
    assert login_response.cookies.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_login_failed(client: AsyncClient):
    user_login_data = {
        "username": "example@mail.ru",
        "password": "password123",
        "grant_type": "password",
    }

    response = await client.post("/api/v1/login/", data=user_login_data)
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient, user_factory: UserFactory):
    users = await user_factory.create_batch_async(10)

    response = await client.get("/api/v1/users/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(users)


@pytest.mark.asyncio
async def test_register_login_logout_flow(client: AsyncClient):
    user_register = UserRegister(email="example@mail.com", password="password123")
    user_register_data = user_register.model_dump()

    register_response = await client.post("/api/v1/register/", json=user_register_data)
    assert register_response.status_code == 201
    response_data = register_response.json()
    assert response_data["email"] == user_register_data["email"]

    user_login_data = {
        "username": user_register.email,
        "password": user_register.password,
        "grant_type": "password",
    }
    login_response = await client.post("/api/v1/login/", data=user_login_data)
    assert login_response.status_code == 200
    login_response_data = login_response.json()
    assert "access_token" in login_response_data
    assert "refresh_token" in login_response_data
    assert login_response_data["user"]["email"] == user_register.email

    # In some way cookies are not saved beetween requests
    refresh_token = login_response.cookies.get("refresh_token")
    assert refresh_token is not None
    client.cookies.set("refresh_token", refresh_token)
    logout_response = await client.post("/api/v1/logout/")
    assert logout_response.status_code == 200
    logout_response_data = logout_response.json()
    assert logout_response_data["message"] == "Successfully logout"


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, auth_header: dict):
    response = await client.get("/api/v1/check/", headers=auth_header)
    assert response.status_code == 200
    response_data = response.json()
    assert "email" in response_data
    assert "id" in response_data
    assert "role" in response_data
    assert "password" not in response_data


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    pass

#REWORK LOGIC DEFINITION NEW PASSWORD
@pytest.mark.asyncio
async def test_change_password(client: AsyncClient, auth_header):
    new_password = "defenitly_new_password_i_promise"
    
    response = await client.patch(
        "/api/v1/change-password/", headers=auth_header, json={"new_password": new_password}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "Password updated successfully"


@pytest.mark.asyncio
async def test_not_authorized(client: AsyncClient):
    response = await client.get("/api/v1/check/")
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "Not authenticated"


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    invalid_token = generate_invalid_token()

    response = await client.get(
        "/api/v1/check/", headers={"Authorization": f"Bearer {invalid_token}"}
    )
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "The token is not valid"


@pytest.mark.asyncio
async def test_expired_token(client: AsyncClient):
    expired_token = generate_expired_token()

    response = await client.get(
        "/api/v1/check/", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    response_data = response.json()
    assert response_data["detail"] == "The token has expired"


@pytest.mark.asyncio
# @pytest.mark.slow
async def test_rate_limiting(client: AsyncClient, auth_header:dict):
    for _ in range(6):
        response = await client.patch("/api/v1/change-password/", headers=auth_header,json={"new_password": "new_password"})
    
    assert response.status_code==429 # type: ignore
        
    for _ in range(6):
        response = await client.post("/api/v1/register/", json={"email": f"test{_}@test.com", "password": "test_password"})
    
    assert response.status_code==429 # type: ignore