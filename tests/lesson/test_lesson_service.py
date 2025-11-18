import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import ConflictException, NotFoundException
from app.domain.lesson.schemas import LessonCreate, LessonUpdate
from app.domain.lesson.service import LessonService
from tests.factories import LessonFactory


@pytest.mark.asyncio
async def test_get_lessons(session: AsyncSession, lesson_factory: LessonFactory):
    created_lessons = await lesson_factory.create_batch_async(2)
    service = LessonService(session)
    lessons = await service.get_all()
    assert len(lessons) == len(created_lessons)


@pytest.mark.asyncio
async def test_get_lesson(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    created_lesson = await lesson_factory.create_async()
    lesson = await service.get_by_id(created_lesson.id)
    assert lesson is not None
    assert lesson.id == created_lesson.id


@pytest.mark.asyncio
async def test_get_lesson_not_found(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    created_lesson = lesson_factory.build()
    lesson = await service.get_by_id(created_lesson.id)
    assert lesson is None


@pytest.mark.asyncio
async def test_create_lesson(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    lesson_instance = lesson_factory.build()
    lesson_in = LessonCreate.model_validate(lesson_instance)

    lesson = await service.create(lesson_in)
    assert lesson.room_id == lesson_in.room_id
    assert lesson.teacher_id == lesson_in.teacher_id
    assert lesson.group_id == lesson_in.group_id
    assert lesson.day_of_week == lesson_in.day_of_week
    assert lesson.time_id == lesson_in.time_id
    assert lesson.subject_id == lesson_in.subject_id
    assert lesson.type == lesson_in.type

    with pytest.raises(ConflictException):
        await service.create(lesson_in)


@pytest.mark.asyncio
async def test_update_lesson(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    created_lesson = await lesson_factory.create_async()
    lesson_in = LessonUpdate(
        time_id=2,
        day_of_week=1,
        type="Лекция",
        subject_id=created_lesson.subject_id,
        teacher_id=created_lesson.teacher_id,
        room_id=created_lesson.room_id,
        group_id=created_lesson.group_id,
    )

    lesson = await service.update(created_lesson.id, lesson_in)
    assert lesson.id == created_lesson.id
    assert lesson.room_id == lesson_in.room_id
    assert lesson.teacher_id == lesson_in.teacher_id
    assert lesson.group_id == lesson_in.group_id
    assert lesson.day_of_week == lesson_in.day_of_week
    assert lesson.time_id == lesson_in.time_id
    assert lesson.subject_id == lesson_in.subject_id
    assert lesson.type == lesson_in.type


@pytest.mark.asyncio
async def test_update_lesson_not_found(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    lesson_instance = lesson_factory.build()
    lesson_in = LessonUpdate(
        time_id=2,
        day_of_week=1,
        type="Лекция",
        subject_id=1,
        teacher_id=1,
        room_id=1,
        group_id=1,
    )

    with pytest.raises(NotFoundException):
        await service.update(lesson_instance.id, lesson_in)


@pytest.mark.asyncio
async def test_update_lesson_conflict(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    created_lessons = await lesson_factory.create_batch_async(2)
    lesson_in = LessonUpdate(
        time_id=created_lessons[1].time_id,
        day_of_week=created_lessons[1].day_of_week,
        type=created_lessons[1].type,
        subject_id=created_lessons[1].subject_id,
        teacher_id=created_lessons[1].teacher_id,
        room_id=created_lessons[1].room_id,
        group_id=created_lessons[1].group_id,
    )

    with pytest.raises(ConflictException):
        await service.update(created_lessons[0].id, lesson_in)


@pytest.mark.asyncio
async def test_delete_lesson(session: AsyncSession, lesson_factory: LessonFactory):
    service = LessonService(session)
    created_lesson = await lesson_factory.create_async()

    lesson = await service.delete(created_lesson.id)
    assert lesson is None

    with pytest.raises(NotFoundException):
        await service.delete(created_lesson.id)
