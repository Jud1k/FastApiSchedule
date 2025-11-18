import random
import pytest

from httpx import AsyncClient
from app.domain.building.schemas import BuildingCreate, BuildingUpdate
from tests.factories import BuildingFactory


@pytest.mark.asyncio
async def test_get_buildings(client: AsyncClient, building_factory: BuildingFactory):
    buildings = await building_factory.create_batch_async(2)

    response = await client.get("/api/v1/building/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(buildings)


@pytest.mark.asyncio
async def test_get_building(client: AsyncClient, building_factory: BuildingFactory):
    building = await building_factory.create_async()

    response = await client.get(f"/api/v1/building/{building.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == building.id
    assert response_data["name"] == building.name
    assert response_data["address"] == building.address


@pytest.mark.asyncio
async def test_get_building_not_found(client:AsyncClient,building_factory:BuildingFactory):
    building_id = random.randint(1,1_000_000)
    response = await client.get(f"/api/v1/building/{building_id}")
    assert response.status_code==404
    response_data=response.json()
    assert response_data["detail"]==f"Building with ID {building_id} not found"
    
    
@pytest.mark.asyncio
async def test_create_building(client: AsyncClient, building_factory: BuildingFactory):
    building_instance = building_factory.build()
    building_in = BuildingCreate.model_validate(building_instance, from_attributes=True)
    building_in_data = building_in.model_dump()

    response = await client.post("/api/v1/building/", json=building_in_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == building_in.name
    assert response_data["address"] == building_in.address


@pytest.mark.asyncio
async def test_update_building(client: AsyncClient, building_factory: BuildingFactory):
    building = await building_factory.create_async()
    building_in = BuildingUpdate(name="New Name", address="New Address")
    building_in_data = building_in.model_dump()

    response = await client.put(f"/api/v1/building/{building.id}", json=building_in_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == building.id
    assert response_data["name"] == building_in.name
    assert response_data["address"] == building_in.address


@pytest.mark.asyncio
async def test_delete_building(client: AsyncClient, building_factory: BuildingFactory):
    building = await building_factory.create_async()

    response = await client.delete(f"/api/v1/building/{building.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_building_not_found(client: AsyncClient, building_factory: BuildingFactory):
    building_id = random.randint(1,1_000_000)

    response = await client.delete(f"/api/v1/building/{building_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"]==f"Building with ID {building_id} not found"