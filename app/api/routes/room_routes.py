from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from app.api.schemas.room import RoomFromDB, RoomToCreate
from app.api.dependencies.service_dep import get_room_service
from app.exceptions import ConflictError, NotFoundError
from app.services.room_service import RoomService

router = APIRouter(prefix="/room", tags=["Rooms🏫"])


@router.get("/search", response_model=list[RoomFromDB])
async def search_rooms_by_name(
    query: str = Query(max_length=50),
    service: RoomService = Depends(get_room_service),
):
    return await service.search_rooms(query=query)


@router.get("/", response_model=list[RoomFromDB])
async def get_all_rooms(
    service: RoomService = Depends(get_room_service),
):
    return await service.get_all()


@router.get("/{room_id}", response_model=RoomFromDB)
async def get_room_by_id(
    room_id: int,
    service: RoomService = Depends(get_room_service),
):
    try:
        return await service.get_one_by_id(room_id=room_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=RoomFromDB)
async def create_room(
    room_in: RoomToCreate,
    service: RoomService = Depends(get_room_service),
):
    try:
        return await service.create(room_in=room_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{room_id}", response_model=RoomFromDB)
async def update_room(
    room_id: int,
    room_in: RoomToCreate,
    service: RoomService = Depends(get_room_service),
):
    try:
        return await service.update(room_id=room_id, room_in=room_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{room_id}")
async def delete_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
):
    try:
        return await service.delete(room_id=room_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
