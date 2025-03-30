from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.room import RoomFromDB,RoomToCreate
from app.db.database import get_async_session
from app.services.room_service import RoomService

router = APIRouter(prefix="/room", tags=["Rooms🏫"])


async def get_room_service(session: AsyncSession = Depends(get_async_session)):
    return RoomService(session)


@router.get("/", response_model=list[RoomFromDB])
async def get_all(service: RoomService = Depends(get_room_service)):
    return await service.get_all()


@router.get("/{room_id}", response_model=RoomFromDB)
async def get_one_by_id(
    room_id: int, service: RoomService = Depends(get_room_service)
):
    return await service.get_one_by_id(room_id)


@router.post("/", response_model=RoomFromDB)
async def create(
    room: RoomToCreate, service: RoomService = Depends(get_room_service)
):
    return await service.create(room)


@router.put("/{room_id}", response_model=RoomFromDB)
async def update(
    room_id: int,
    room: RoomToCreate,
    service: RoomService = Depends(get_room_service),
):
    return await service.update(room_id, room)


@router.delete("/")
async def delete(
    room_id: int | None = None,
    delete_all: bool = False,
    service: RoomService = Depends(get_room_service),
):
    if not room_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(room_id, delete_all)
