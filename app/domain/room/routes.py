from fastapi import APIRouter, status
from fastapi.params import Query

from app.core.deps.service import RoomServiceDep
from app.exceptions import NotFoundException
from app.domain.room.schemas import RoomRead, RoomCreate, RoomUpdate, RoomReadMinimal

router = APIRouter(prefix="/room", tags=["Rooms🏫"])


@router.get("/search", response_model=list[RoomReadMinimal])
async def search_rooms_by_name(
    service:RoomServiceDep,
    query = Query(max_length=50),
):
    return await service.search_rooms(query=str(query))


@router.get("/", response_model=list[RoomRead])
async def get_all_rooms(
    service:RoomServiceDep
):
    return await service.get_all()


@router.get("/{room_id}", response_model=RoomRead)
async def get_room_by_id(
    room_id: int,
    service:RoomServiceDep
):
    room = await service.get_by_id(room_id=room_id)
    if not room:
        raise NotFoundException("Room",room_id)
    return room


@router.post("/", response_model=RoomReadMinimal,status_code=status.HTTP_201_CREATED)
async def create_room(
    room_in: RoomCreate,
    service:RoomServiceDep
):
    
    return await service.create(room_in=room_in)


@router.put("/{room_id}", response_model=RoomReadMinimal)
async def update_room(
    room_id: int,
    room_in: RoomUpdate,
    service:RoomServiceDep
):
    return await service.update(room_id=room_id, room_in=room_in)


@router.delete("/{room_id}", response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    room_id: int,
    service:RoomServiceDep
):
    return await service.delete(room_id=room_id)

