import random
import pytest

from httpx import AsyncClient

from app.domain.subject.schemas import SubjectCreate, SubjectUpdate
from tests.factories import SubjectFactory


@pytest.mark.asyncio
async def test_get_subjects(client:AsyncClient,subject_factory:SubjectFactory):
    subjects = await subject_factory.create_batch_async(2)
    
    response = await client.get("/api/v1/subject/")
    assert response.status_code==200
    response_data = response.json()
    assert len(response_data)==len(subjects)
    
    
@pytest.mark.asyncio
async def test_get_subject(client:AsyncClient,subject_factory:SubjectFactory):
    subject = await subject_factory.create_async()
    
    response = await client.get(f"/api/v1/subject/{subject.id}")
    assert response.status_code==200
    response_data=response.json()
    assert response_data["id"]==subject.id
    assert response_data["name"]==subject.name
    assert response_data["total_hours"]==subject.total_hours
    assert response_data["is_optional"]==subject.is_optional
    assert response_data["semester"]==subject.semester
    
    
@pytest.mark.asyncio
async def test_get_subject_not_found(client:AsyncClient,subject_factory:SubjectFactory):
    subject_id = random.randint(1,1_000_000) 
    
    response = await client.get(f"/api/v1/subject/{subject_id}")
    assert response.status_code==404
    response_data=response.json()
    assert response_data["detail"]==f"Subject with ID {subject_id} not found"
    
    
@pytest.mark.asyncio
async def test_create_subject(client:AsyncClient):
    subject_in = SubjectCreate(name="New Name", semester=2,total_hours=108,is_optional=True)
    subject_in_data = subject_in.model_dump()
    
    response = await client.post("/api/v1/subject/",json=subject_in_data)
    assert response.status_code==201
    response_data = response.json()
    assert response_data["name"]==subject_in.name
    assert response_data["total_hours"]==subject_in.total_hours
    assert response_data["is_optional"]==subject_in.is_optional
    assert response_data["semester"]==subject_in.semester 
    
    
@pytest.mark.asyncio
async def test_update_subject(client:AsyncClient,subject_factory:SubjectFactory):
    subject = await subject_factory.create_async()
    subject_in = SubjectUpdate(name="New Name", semester=2,total_hours=108,is_optional=True)
    subject_in_data = subject_in.model_dump()
    
    response = await client.put(f"/api/v1/subject/{subject.id}",json=subject_in_data)
    assert response.status_code==200
    response_data=response.json()
    assert response_data["name"]==subject_in.name
    assert response_data["total_hours"]==subject_in.total_hours
    assert response_data["is_optional"]==subject_in.is_optional
    assert response_data["semester"]==subject_in.semester 
    
    
@pytest.mark.asyncio
async def test_delete_subject(client:AsyncClient,subject_factory:SubjectFactory):
    subject = await subject_factory.create_async()
    
    response = await client.delete(f"/api/v1/subject/{subject.id}")
    assert response.status_code==204


@pytest.mark.asyncio
async def test_delete_subject_not_found(client:AsyncClient,subject_factory:SubjectFactory):
    subject_id = random.randint(1,1_000_000) 
    
    response = await client.delete(f"/api/v1/subject/{subject_id}")
    assert response.status_code==404
    response_data = response.json()
    assert response_data["detail"]==f"Subject with ID {subject_id} not found"