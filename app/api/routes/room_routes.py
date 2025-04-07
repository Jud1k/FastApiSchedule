from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.room import RoomFromDB, RoomToCreate
from app.api.dependecy import get_async_session, get_room_service
from app.services.room_service import RoomService

router = APIRouter(prefix="/room", tags=["Rooms🏫"])


@router.get("/", response_model=list[RoomFromDB])
async def get_all(
    service: RoomService = Depends(get_room_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all(session=session)


@router.get("/{room_id}", response_model=RoomFromDB)
async def get_one_by_id(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_one_by_id(session=session, room_id=room_id)


@router.post("/", response_model=RoomFromDB)
async def create(
    room: RoomToCreate,
    service: RoomService = Depends(get_room_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create(session=session, room_data=room)


@router.put("/{room_id}", response_model=RoomFromDB)
async def update(
    room_id: int,
    room: RoomToCreate,
    service: RoomService = Depends(get_room_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.update(session=session, room_id=room_id, room_data=room)


@router.delete("/")
async def delete(
    room_id: int | None = None,
    delete_all: bool = False,
    service: RoomService = Depends(get_room_service),
    session: AsyncSession = Depends(get_async_session),
):
    if not room_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(session=session, room_id=room_id, delete_all=delete_all)
