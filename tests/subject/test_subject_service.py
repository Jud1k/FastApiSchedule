import pytest
import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.domain.subject.schemas import SubjectCreate, SubjectUpdate
from app.domain.subject.service import SubjectService
from tests.factories import SubjectFactory


@pytest.mark.asyncio
async def test_get_subjects(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    created_subjects = await subject_factory.create_batch_async(2)
    
    subjects = await service.get_all()
    assert len(subjects)==len(created_subjects)
    
    
@pytest.mark.asyncio
async def test_get_subject(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    created_subject = await subject_factory.create_async()

    subject = await service.get_by_id(created_subject.id)
    assert subject is not None
    assert subject.id == created_subject.id


@pytest.mark.asyncio
async def test_get_subject_not_found(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    subject_id = random.randint(1,1_000_000)    
    subject = await service.get_by_id(subject_id)
    assert subject is None
    
@pytest.mark.asyncio
async def test_create_subject(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    subject_instance = subject_factory.build()
    subject_in = SubjectCreate.model_validate(subject_instance, from_attributes=True)

    subject = await service.create(subject_in)
    assert subject.name == subject_in.name
    with pytest.raises(ConflictException):
        await service.create(subject_in)


@pytest.mark.asyncio
async def test_update_subject(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    created_subject = await subject_factory.create_async()
    subject_in = SubjectUpdate(name="New Name", total_hours=108, semester=6, is_optional=False)

    subject = await service.update(created_subject.id,subject_in)
    assert subject.id==created_subject.id
    assert subject.name==subject_in.name
    
    
@pytest.mark.asyncio
async def test_update_subject_not_found(session:AsyncSession,subject_factory:SubjectFactory):
    service = SubjectService(session)
    subject_instance = subject_factory.build()
    subject_in = SubjectUpdate(name="New Name", total_hours=108, semester=6, is_optional=False)
    
    with pytest.raises(NotFoundException):
        await service.update(subject_instance.id,subject_in)
        
        
@pytest.mark.asyncio
async def test_update_subject_conflict(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    created_subjects = await subject_factory.create_batch_async(2)
    subject_in = SubjectUpdate.model_validate(created_subjects[0],from_attributes=True)
    
    with pytest.raises(ConflictException):
        await service.update(created_subjects[1].id,subject_in)
    
        
@pytest.mark.asyncio
async def test_delete_subject(session: AsyncSession, subject_factory: SubjectFactory):
    service = SubjectService(session)
    created_subject = await subject_factory.create_async()
    
    subject = await service.delete(created_subject.id)
    assert subject is None
    
    with pytest.raises(NotFoundException):
        await service.delete(created_subject.id)

