import random
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import ConflictException, NotFoundException
from app.domain.room.schemas import RoomCreate, RoomUpdate
from app.domain.room.service import RoomService
from tests.factories import RoomFactory


@pytest.mark.asyncio
async def test_get_rooms(session: AsyncSession, room_factory: RoomFactory):
    service = RoomService(session)
    created_rooms = await room_factory.create_batch_async(2)
    
    rooms = await service.get_all()
    assert len(rooms) == len(created_rooms)


@pytest.mark.asyncio
async def test_get_room(session: AsyncSession, room_factory: RoomFactory):
    created_room = await room_factory.create_async()
    service = RoomService(session)

    room = await service.get_by_id(created_room.id)
    assert room is not None
    assert created_room.id == room.id


@pytest.mark.asyncio
async def test_get_room_not_found(session: AsyncSession, room_factory: RoomFactory):
    service = RoomService(session)
    room_id = random.randint(1, 1_000_000)
    
    room = await service.get_by_id(room_id)
    assert room is None


@pytest.mark.asyncio
async def test_create_room(session: AsyncSession, room_factory: RoomFactory):
    service = RoomService(session)
    room_instance = room_factory.build()
    room_in = RoomCreate.model_validate(room_instance)
    room = await service.create(room_in)
    assert room.name == room_in.name
    assert room.status == room_in.status
    assert room.capacity == room_in.capacity
    assert room.floor == room_in.floor
    assert room.building_id == room_in.building_id
    
    with pytest.raises(ConflictException):
        await service.create(room_in)


@pytest.mark.asyncio
async def test_update_room(session: AsyncSession, room_factory: RoomFactory):
    service = RoomService(session)
    created_room = await room_factory.create_async()
    room_in = RoomUpdate(
        name="New Name", status=1, capacity=20, floor=5, building_id=1
    )

    room = await service.update(created_room.id, room_in)
    assert room.id==created_room.id
    assert room.name==room_in.name
    assert room.status==room_in.status
    assert room.capacity==room_in.capacity
    assert room.floor==room_in.floor
    assert room.building_id==room_in.building_id

@pytest.mark.asyncio
async def test_update_room_not_found(session:AsyncSession,room_factory:RoomFactory):
    service = RoomService(session)
    room_instance = room_factory.build()
    room_in = RoomUpdate(
        name="New Name", status=1, capacity=20, floor=5, building_id=1
    )
    
    with pytest.raises(NotFoundException):
        await service.update(room_instance.id,room_in)
        
        
@pytest.mark.asyncio
async def test_update_room_conflict(session:AsyncSession,room_factory:RoomFactory):
    service = RoomService(session)
    created_rooms = await room_factory.create_batch_async(2)
    room_in = RoomUpdate.model_validate(created_rooms[0])
    
    with pytest.raises(ConflictException):
        await service.update(created_rooms[1].id,room_in)    

@pytest.mark.asyncio
async def test_delete_room(session: AsyncSession, room_factory: RoomFactory):
    service = RoomService(session)
    created_room = await room_factory.create_async()

    room = await service.delete(created_room.id)
    assert room is None
    
    with pytest.raises(NotFoundException):
        await service.delete(created_room.id)
