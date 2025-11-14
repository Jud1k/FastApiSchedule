import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictErr, NotFoundErr
from app.teacher.service import TeacherService
from tests.factories import TeacherFactory
from app.teacher.schemas import TeacherCreate, TeacherUpdate


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
    teacher_instance = teacher_factory.build()

    teacher = await service.get_by_id(teacher_instance.id)
    assert teacher is None


@pytest.mark.asyncio
async def test_create_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    teacher_in = TeacherCreate(
        name="New Teacher",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )

    teacher = await service.create(teacher_in)
    assert teacher.name == teacher_in.name
    assert teacher.email == teacher_in.email
    assert teacher.phone == teacher_in.phone
    assert teacher.department == teacher_in.department
    assert teacher.title == teacher_in.title

    with pytest.raises(ConflictErr):
        await service.create(teacher_in)


@pytest.mark.asyncio
async def test_update_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher = await teacher_factory.create_async()
    teacher_in = TeacherUpdate(
        name="New Teacher",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )

    teacher = await service.update(created_teacher.id,teacher_in)
    assert teacher.id==created_teacher.id
    assert teacher.name == teacher_in.name
    assert teacher.email == teacher_in.email
    assert teacher.phone == teacher_in.phone
    assert teacher.department == teacher_in.department
    assert teacher.title == teacher_in.title
    
    
@pytest.mark.asyncio
async def test_update_teacher_not_found(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    teacher_instance = teacher_factory.build()
    teacher_in = TeacherUpdate(
        name="New Teacher",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Title",
    )
    with pytest.raises(NotFoundErr):
        await service.update(teacher_instance.id,teacher_in)
    

@pytest.mark.asyncio
async def test_update_teacher_conflict(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teachers = await teacher_factory.create_batch_async(2)
    teacher_in = TeacherUpdate(
        name="New Teacher",
        email="example@mail.com",
        phone=created_teachers[0].phone,
        department="New Department",
        title="New Title",
    )

    with pytest.raises(ConflictErr):
        await service.update(created_teachers[1].id,teacher_in)
        
        
@pytest.mark.asyncio
async def test_delete_teacher(session: AsyncSession, teacher_factory: TeacherFactory):
    service = TeacherService(session)
    created_teacher = await teacher_factory.create_async()

    teacher = await service.delete(created_teacher.id)
    assert teacher is None

    with pytest.raises(NotFoundErr):
        await service.delete(created_teacher.id)
