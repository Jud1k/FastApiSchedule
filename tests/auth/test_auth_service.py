import uuid
import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.auth.schemas import UserCreate
from app.domain.auth.service import AuthService
from app.cache.custom_redis import CustomRedis
from app.domain.auth.utils import get_password_hash, verify_password
from tests.factories import UserFactory


@pytest.mark.asyncio
async def test_get_all_users(session: AsyncSession, redis: CustomRedis, user_factory: UserFactory):
    service = AuthService(session, redis)
    created_users = await user_factory.create_batch_async(2)

    users = await service.get_all()
    assert len(users) == len(created_users)


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession, redis: CustomRedis, user_factory: UserFactory):
    service = AuthService(session, redis)
    created_user = await user_factory.create_async()

    user = await service.get_by_id(created_user.id)
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email
    assert user.password == created_user.password


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(session: AsyncSession, redis: CustomRedis):
    service = AuthService(session, redis)
    user_id = uuid.uuid4()
    
    user = await service.get_by_id(user_id)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_email(
    session: AsyncSession, redis: CustomRedis, user_factory: UserFactory
):
    service = AuthService(session, redis)
    created_user = await user_factory.create_async()

    user = await service.get_by_email(created_user.email)
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email
    assert user.password == created_user.password


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(session: AsyncSession, redis: CustomRedis):
    service = AuthService(session, redis)
    email = "nonexistent@example.com"
    
    user = await service.get_by_email(email)
    assert user is None
    
    
@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, redis: CustomRedis):
    service = AuthService(session, redis)
    password = "password123"
    user_in = UserCreate(email="test@example.com", password=password)

    user = await service.create(user_in)
    assert user.email == user_in.email
    assert verify_password(password, user.password)


@pytest.mark.asyncio
async def test_update_user_password(
    session: AsyncSession, redis: CustomRedis, user_factory: UserFactory
):
    service = AuthService(session, redis)
    password = get_password_hash("OldPassword")
    created_user = await user_factory.create_async(password=password)

    new_password = "NewPassword"
    result = await service.update_user_password(user_id=created_user.id, new_password=new_password)
    assert result is None


