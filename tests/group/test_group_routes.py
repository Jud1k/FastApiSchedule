import random
import pytest
from httpx import AsyncClient

from app.domain.group.schemas import GroupCreate,GroupUpdate
from tests.factories import GroupFactory


@pytest.mark.asyncio
async def test_get_groups(client:AsyncClient,group_factory:GroupFactory):   
    groups = await group_factory.create_batch_async(2)
    
    response = await client.get("/api/v1/group/")
    assert response.status_code==200
    response_data = response.json()
    assert len(response_data)==len(groups)


@pytest.mark.asyncio
async def test_get_group(client:AsyncClient,group_factory:GroupFactory):
    group = await group_factory.create_async()

    response = await client.get(f"/api/v1/group/{group.id}")
    assert response.status_code==200
    response_data=response.json()
    assert response_data["id"]==group.id
    assert response_data["name"]==group.name
    assert response_data["course"]==group.course
    assert response_data["institute"]==group.institute
    

@pytest.mark.asyncio
async def test_get_groups_summary(client:AsyncClient,group_factory:GroupFactory):
    groups = await group_factory.create_batch_async(2)
    
    response = await client.get("/api/v1/group/summary/")
    assert response.status_code==200
    response_data = response.json()
    assert len(response_data)==len(groups)
    
    
@pytest.mark.asyncio
async def test_get_group_not_found(client:AsyncClient):
    group_id = random.randint(1,1_000_000)
    
    response = await client.get(f"/api/v1/group/{group_id}")
    assert response.status_code==404
    response_data = response.json()
    assert response_data["detail"]==f"Group with ID {group_id} not found"
    
    
@pytest.mark.asyncio
async def test_create_group(client:AsyncClient):
    group_in = GroupCreate(name="Test Group",course=1,institute="Test Institute")
    group_in_data = group_in.model_dump()
    
    response = await client.post("/api/v1/group/",json=group_in_data)
    assert response.status_code==201
    respone_data = response.json()
    assert respone_data["name"]==group_in.name
    assert respone_data["course"]==group_in.course
    assert respone_data["institute"]==group_in.institute
    
    
@pytest.mark.asyncio
async def test_update_group(client:AsyncClient,group_factory:GroupFactory):
    group = await group_factory.create_async()
    group_in = GroupUpdate(name="New Name",course=1,institute="New Institute")
    group_in_data = group_in.model_dump()
    
    response = await client.put(f"/api/v1/group/{group.id}",json=group_in_data)
    assert response.status_code==200
    response_data = response.json()
    assert response_data["id"]==group.id
    assert response_data["name"]==group_in.name
    assert response_data["course"]==group_in.course
    assert response_data["institute"]==group_in.institute
    

@pytest.mark.asyncio
async def test_delete_group(client:AsyncClient,group_factory:GroupFactory):
    group = await group_factory.create_async()
    
    response = await client.delete(f"/api/v1/group/{group.id}")
    assert response.status_code==204

@pytest.mark.asyncio
async def test_delete_group_not_found(client:AsyncClient,group_factory:GroupFactory):
    group_id = random.randint(1,1_000_000)
    
    reponse = await client.delete(f"/api/v1/group/{group_id}")
    assert reponse.status_code==404
    response_data = reponse.json()
    assert response_data["detail"]==f"Group with ID {group_id} not found"