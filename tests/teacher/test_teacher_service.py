import random
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.domain.teacher.service import TeacherService
from tests.factories import TeacherFactory
from app.domain.teacher.schemas import TeacherCreate, TeacherUpdate


@pytest.mark.asyncio
async def test_get_teachers(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teachers = await teacher_factory.create_batch_async(2)

    teachers = await service.get_all()
    assert len(created_teachers) == len(teachers)


@pytest.mark.asyncio
async def test_get_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher = await teacher_factory.create_async()

    teacher = await service.get_by_id(created_teacher.id)
    assert teacher is not None
    assert created_teacher.id == teacher.id


@pytest.mark.asyncio
async def test_get_teacher_not_found(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    teacher_id = random.randint(1, 1_000_000)

    teacher = await service.get_by_id(teacher_id)
    assert teacher is None


@pytest.mark.asyncio
async def test_create_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    teacher_in = TeacherCreate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )

    teacher = await service.create(teacher_in)
    assert teacher.first_name == teacher_in.first_name
    assert teacher.middle_name == teacher_in.middle_name
    assert teacher.last_name == teacher_in.last_name
    assert teacher.email == teacher_in.email
    assert teacher.phone == teacher_in.phone
    assert teacher.department == teacher_in.department
    assert teacher.title == teacher_in.title

    with pytest.raises(ConflictException):
        await service.create(teacher_in)


@pytest.mark.asyncio
async def test_update_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher = await teacher_factory.create_async()
    teacher_in = TeacherUpdate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )

    teacher = await service.update(created_teacher.id, teacher_in)
    assert teacher.id == created_teacher.id
    assert teacher.first_name == teacher_in.first_name
    assert teacher.middle_name == teacher_in.middle_name
    assert teacher.last_name == teacher_in.last_name
    assert teacher.email == teacher_in.email
    assert teacher.phone == teacher_in.phone
    assert teacher.department == teacher_in.department
    assert teacher.title == teacher_in.title


@pytest.mark.asyncio
async def test_update_teacher_not_found(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    teacher_instance = teacher_factory.build()
    teacher_in = TeacherUpdate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )
    with pytest.raises(NotFoundException):
        await service.update(teacher_instance.id, teacher_in)


@pytest.mark.asyncio
async def test_update_teacher_conflict(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher1 = await teacher_factory.create_async(phone="+71234567890")
    created_teacher2 = await teacher_factory.create_async(phone="")
    teacher_in = TeacherUpdate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone=created_teacher1.phone,
        department="New Department",
        title="New Title",
    )

    with pytest.raises(ConflictException):
        await service.update(created_teacher2.id, teacher_in)


@pytest.mark.asyncio
async def test_delete_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher = await teacher_factory.create_async()

    teacher = await service.delete(created_teacher.id)
    assert teacher is None

    with pytest.raises(NotFoundException):
        await service.delete(created_teacher.id)
