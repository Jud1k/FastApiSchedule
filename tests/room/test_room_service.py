import pytest

from app.api.schemas.room import RoomToCreate
from app.exceptions import NotFoundError
from app.services.room_service import RoomService


@pytest.mark.asyncio
async def test_get_all(session):
    service = RoomService(session)
    rooms = await service.get_all()
    assert len(rooms) < 1


@pytest.mark.asyncio
async def test_get(session, room):
    service = RoomService(session)
    with pytest.raises(NotFoundError):
        await service.get_one_by_id(room_id=room.id)


@pytest.mark.asyncio
async def test_create(session, room):
    service = RoomService(session)
    room_in = RoomToCreate(name=room.name)
    t_room = await service.create(room_in=room_in)
    assert t_room


# @pytest.mark.asyncio
# async def test_update(session,room):
#     service=RoomService(session)
#     room_in=RoomToCreate(name='1')
#     t_room=await service.update()


# @pytest.mark.asyncio
# async def test_4(session):
#     pass
