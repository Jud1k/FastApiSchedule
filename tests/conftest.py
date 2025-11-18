from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest

from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
    create_async_engine,
)
from app.cache.custom_redis import CustomRedis
from app.db.database import Base
from tests.factories import (
    SubjectFactory,
    RoomFactory,
    BuildingFactory,
    TeacherFactory,
    LessonFactory,
    GroupFactory,
    UserFactory
)


@pytest.fixture(scope="function",autouse=True)
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def session_maker(engine) -> async_sessionmaker:
    return async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )


@pytest.fixture
async def session(session_maker) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
            await session.rollback()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()



@pytest.fixture(scope="function")
async def redis()->AsyncGenerator[CustomRedis,None]:
    from app.core.config import settings
    
    redis_client = CustomRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,ssl=settings.REDIS_SSL)
    async with redis_client as rc:
        try:
            yield rc
        finally:
            await rc.delete_all_keys()
    
    
@pytest.fixture(scope="function")
async def client(session:AsyncSession,redis:CustomRedis) -> AsyncGenerator[AsyncClient, None]:
    import logging
    from app.main import app
    from app.limiter import limiter
    from app.db.database import get_db
    from app.cache.manager import get_redis
    
    logging.getLogger("httpx").disabled = True
    limiter.reset()
    app.dependency_overrides[get_db] = lambda:session
    app.dependency_overrides[get_redis] = lambda:redis
    try:
        async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def auth_header(client:AsyncClient):
    email = "test@test.com"
    password = "test"
    
    response = await client.post("/api/v1/register/",json={"email":email,"password":password})
    assert response.status_code==201
    
    response = await client.post("/api/v1/login/",data={"username":email,"password":password,"grant_type":"password"})
    assert response.status_code==200
    
    refresh_token = response.cookies.get("refresh_token")
    assert refresh_token is not None
    client.cookies.set("refresh_token",refresh_token)
    
    access_token = response.json()["access_token"]
    return {"Authorization":f"Bearer {access_token}"}


@pytest.fixture
def subject_factory(session):
    class SessionSubjectFactory(SubjectFactory):
        __async_session__ = session

    return SessionSubjectFactory


@pytest.fixture
def room_factory(session):
    class SessionRoomFactory(RoomFactory):
        __async_session__ = session

    return SessionRoomFactory


@pytest.fixture
def building_factory(session):
    class SessionBuildingFactory(BuildingFactory):
        __async_session__ = session

    return SessionBuildingFactory


@pytest.fixture
def teacher_factory(session):
    class SessionTeacherFactory(TeacherFactory):
        __async_session__ = session

    return SessionTeacherFactory


@pytest.fixture
def group_factory(session):
    class SessionGroupFactory(GroupFactory):
        __async_session__ = session

    return SessionGroupFactory


@pytest.fixture
def lesson_factory(session):
    class SessionLessonFactory(LessonFactory):
        __async_session__ = session

    return SessionLessonFactory


@pytest.fixture
def user_factory(session): 
    class SessionUserFactory(UserFactory):
        __async_session__ = session

    return SessionUserFactory
