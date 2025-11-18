import random
import pytest
from httpx import AsyncClient

from tests.factories import TeacherFactory
from app.domain.teacher.schemas import TeacherCreate, TeacherUpdate


@pytest.mark.asyncio
async def test_get_teachers(client: AsyncClient, teacher_factory: TeacherFactory):
    teachers = await teacher_factory.create_batch_async(2)

    response = await client.get("/api/v1/teacher/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(teachers)


@pytest.mark.asyncio
async def test_get_teacher(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher = await teacher_factory.create_async()

    response = await client.get(f"/api/v1/teacher/{teacher.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == teacher.id
    assert response_data["first_name"] == teacher.first_name
    assert response_data["middle_name"] == teacher.middle_name
    assert response_data["last_name"] == teacher.last_name
    assert response_data["department"] == teacher.department
    assert response_data["email"] == teacher.email
    assert response_data["phone"] == teacher.phone
    assert response_data["title"] == teacher.title


@pytest.mark.asyncio
async def test_get_teacher_not_found(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher_id = random.randint(1, 1_000_000)

    response = await client.get(f"/api/v1/teacher/{teacher_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == f"Teacher with ID {teacher_id} not found"


@pytest.mark.asyncio
async def test_create_teacher(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher_in = TeacherCreate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Titile",
    )
    teacher_in_data = teacher_in.model_dump()

    response = await client.post("/api/v1/teacher/",json=teacher_in_data)
    assert response.status_code==201
    response_data = response.json()
    assert response_data["first_name"] == teacher_in.first_name
    assert response_data["middle_name"] == teacher_in.middle_name
    assert response_data["last_name"] == teacher_in.last_name
    assert response_data["department"] == teacher_in.department
    assert response_data["email"] == teacher_in.email
    assert response_data["phone"] == teacher_in.phone
    assert response_data["title"] == teacher_in.title
    
    
@pytest.mark.asyncio
async def test_update_teacher(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher = await teacher_factory.create_async()
    teacher_in = TeacherUpdate(
        first_name="New First Name",
        middle_name="New Middle Name",
        last_name="New Last Name",
        email="example@mail.com",
        phone="+71234567890",
        department="New Department",
        title="New Titile",
    )
    teacher_in_data = teacher_in.model_dump()

    response = await client.put(f"/api/v1/teacher/{teacher.id}",json=teacher_in_data)
    assert response.status_code==200
    response_data = response.json()
    assert response_data["id"] == teacher.id
    assert response_data["first_name"] == teacher_in.first_name
    assert response_data["middle_name"] == teacher_in.middle_name
    assert response_data["last_name"] == teacher_in.last_name
    assert response_data["department"] == teacher_in.department
    assert response_data["email"] == teacher_in.email
    assert response_data["phone"] == teacher_in.phone
    assert response_data["title"] == teacher_in.title
    
@pytest.mark.asyncio
async def test_delete_teacher(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher = await teacher_factory.create_async()

    response = await client.delete(f"/api/v1/teacher/{teacher.id}")
    assert response.status_code==204
    
    
@pytest.mark.asyncio
async def test_delete_teacher_not_found(client: AsyncClient, teacher_factory: TeacherFactory):
    teacher_id = random.randint(1,1_000_000)

    response = await client.delete(f"/api/v1/teacher/{teacher_id}")
    assert response.status_code==404
    response_data=response.json()
    assert response_data["detail"]==f"Teacher with ID {teacher_id} not found"