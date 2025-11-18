import random
import pytest

from httpx import AsyncClient
from app.domain.lesson.schemas import LessonCreate, LessonUpdate
from tests.factories import LessonFactory


@pytest.mark.asyncio
async def test_get_lessons_by_group_id(client: AsyncClient, lesson_factory: LessonFactory):
    lesson = await lesson_factory.create_async()

    response = await client.get(f"/api/v1/lesson/?group={lesson.group_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["group"]
    assert response_data[0]["room"]
    assert response_data[0]["teacher"]
    assert response_data[0]["subject"]
    assert response_data[0]["type"] == lesson.type
    assert response_data[0]["day_of_week"] == lesson.day_of_week
    assert response_data[0]["time_id"] == lesson.time_id


@pytest.mark.asyncio
async def test_get_lessons_by_teacher_id(client: AsyncClient, lesson_factory: LessonFactory):
    lesson = await lesson_factory.create_async()

    response = await client.get(f"/api/v1/lesson/?teacher={lesson.teacher_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["group"]
    assert response_data[0]["room"]
    assert response_data[0]["teacher"]
    assert response_data[0]["subject"]
    assert response_data[0]["type"] == lesson.type
    assert response_data[0]["day_of_week"] == lesson.day_of_week
    assert response_data[0]["time_id"] == lesson.time_id


@pytest.mark.asyncio
async def test_get_lessons_by_room_id(client: AsyncClient, lesson_factory: LessonFactory):
    lesson = await lesson_factory.create_async()

    response = await client.get(f"/api/v1/lesson/?room={lesson.room_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["group"]
    assert response_data[0]["room"]
    assert response_data[0]["teacher"]
    assert response_data[0]["subject"]
    assert response_data[0]["type"] == lesson.type
    assert response_data[0]["day_of_week"] == lesson.day_of_week
    assert response_data[0]["time_id"] == lesson.time_id


@pytest.mark.asyncio
async def test_get_lessons_not_query(client: AsyncClient):
    response = await client.get("/api/v1/lesson/")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_lessons_extra_query(client: AsyncClient, lesson_factory: LessonFactory):
    lesson_instance = lesson_factory.build()

    response = await client.get(
        f"/api/v1/lesson/?group={lesson_instance.group_id}&room={lesson_instance.room_id}&teacher={lesson_instance.teacher_id}"
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_lesson(client: AsyncClient):
    lesson_in = LessonCreate(
        time_id=2,
        day_of_week=1,
        type="Лекция",
        subject_id=1,
        teacher_id=1,
        room_id=1,
        group_id=1,
    )
    lesson_in_data = lesson_in.model_dump()

    response = await client.post("/api/v1/lesson/", json=lesson_in_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["time_id"] == lesson_in.time_id
    assert response_data["type"] == lesson_in.type
    assert response_data["day_of_week"] == lesson_in.day_of_week
    assert response_data["subject_id"] == lesson_in.subject_id
    assert response_data["teacher_id"] == lesson_in.teacher_id
    assert response_data["room_id"] == lesson_in.room_id
    assert response_data["group_id"] == lesson_in.group_id


@pytest.mark.asyncio
async def test_update_lesson(client: AsyncClient, lesson_factory: LessonFactory):
    lesson = await lesson_factory.create_async(time_id=2)
    lesson_in = LessonUpdate(
        time_id=3,
        day_of_week=1,
        type="Лекция",
        subject_id=1,
        teacher_id=1,
        room_id=1,
        group_id=1,
    )
    lesson_in_data = lesson_in.model_dump()

    response = await client.put(f"/api/v1/lesson/{lesson.id}", json=lesson_in_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == lesson.id
    assert response_data["time_id"] == lesson_in.time_id
    assert response_data["type"] == lesson_in.type
    assert response_data["day_of_week"] == lesson_in.day_of_week
    assert response_data["subject_id"] == lesson_in.subject_id
    assert response_data["teacher_id"] == lesson_in.teacher_id
    assert response_data["room_id"] == lesson_in.room_id
    assert response_data["group_id"] == lesson_in.group_id


@pytest.mark.asyncio
async def test_delete_lesson(client: AsyncClient, lesson_factory: LessonFactory):
    lesson = await lesson_factory.create_async()

    response = await client.delete(f"/api/v1/lesson/{lesson.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_lesson_not_found(client: AsyncClient):
    lesson_id = random.randint(1, 1_000_000)

    response = await client.delete(f"/api/v1/lesson/{lesson_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == f"Lesson with ID {lesson_id} not found"
