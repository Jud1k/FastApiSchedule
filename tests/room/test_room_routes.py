import pytest
import random

from httpx import AsyncClient
from tests.factories import RoomFactory

from app.domain.room.schemas import RoomCreate, RoomUpdate


@pytest.mark.asyncio
async def test_get_rooms(client: AsyncClient, room_factory: RoomFactory):
    lessons = await room_factory.create_batch_async(2)

    response = await client.get("/api/v1/room/")
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == len(lessons)


@pytest.mark.asyncio
async def test_get_room(client: AsyncClient, room_factory: RoomFactory):
    room = await room_factory.create_async()

    response = await client.get(f"/api/v1/room/{room.id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == room.id
    assert response_data["name"] == room.name
    assert response_data["building_id"] == room.building_id
    assert response_data["capacity"] == room.capacity
    assert response_data["floor"] == room.floor
    assert response_data["status"] == room.status


@pytest.mark.asyncio
async def test_get_room_not_found(client: AsyncClient, room_factory: RoomFactory):
    room_id = random.randint(1, 1_000_000)

    response = await client.get(f"/api/v1/room/{room_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == f"Room with ID {room_id} not found"


@pytest.mark.asyncio
async def test_create_room(client: AsyncClient):
    room_in = RoomCreate(name="New Room", building_id=1, capacity=100, floor=1, status=0)
    room_in_data = room_in.model_dump()

    response = await client.post("/api/v1/room/", json=room_in_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == room_in.name
    assert response_data["building_id"] == room_in.building_id
    assert response_data["capacity"] == room_in.capacity
    assert response_data["floor"] == room_in.floor
    assert response_data["status"] == room_in.status


@pytest.mark.asyncio
async def test_update_room(client: AsyncClient, room_factory: RoomFactory):
    room = await room_factory.create_async()
    room_in = RoomUpdate(name="Updated Room", building_id=2, capacity=200, floor=2, status=1)
    room_in_data = room_in.model_dump()

    response = await client.put(f"/api/v1/room/{room.id}", json=room_in_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == room_in.name
    assert response_data["building_id"] == room_in.building_id
    assert response_data["capacity"] == room_in.capacity
    assert response_data["floor"] == room_in.floor
    assert response_data["status"] == room_in.status
    
    
@pytest.mark.asyncio
async def test_delete_room(client: AsyncClient, room_factory: RoomFactory):
    room = await room_factory.create_async()

    response = await client.delete(f"/api/v1/room/{room.id}")
    assert response.status_code == 204
    
    
@pytest.mark.asyncio
async def test_delete_room_not_found(client: AsyncClient, room_factory: RoomFactory):
    room_id = random.randint(1, 1_000_000)

    response = await client.delete(f"/api/v1/room/{room_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data["detail"] == f"Room with ID {room_id} not found"