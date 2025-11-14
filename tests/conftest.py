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
from app.core.database import Base
from tests.factories import (
    SubjectFactory,
    RoomFactory,
    BuildingFactory,
    TeacherFactory,
    LessonFactory,
    GroupFactory,
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
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    from app.main import app
    from app.core.database import get_db

    app.dependency_overrides[get_db] = lambda:session
    try:
        async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


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
