import logging
from app.api.schemas.room import RoomFromDB, RoomToCreate
from app.repositories.repository import RoomRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, session: AsyncSession):
        self.repo = RoomRepository(session)

    async def get_all(self) -> list[RoomFromDB]:
        return await self.repo.get_all()

    async def get_one_by_id(self, room_id: int) -> RoomFromDB:
        record = await self.repo.get_one_or_none_by_id(room_id)
        if not record:
            raise HTTPException(
                status_code=404, detail=f"Record with {room_id} id does not exist"
            )
        return record

    async def create(self, room_data: RoomToCreate) -> RoomFromDB:
        data = room_data.model_dump()
        try:
            return await self.repo.create(data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail="Room with this name alredy exist",
            )

    async def update(self, room_id: int | None, room_data: RoomToCreate) -> RoomFromDB:
        room = await self.repo.get_one_or_none_by_id(room_id)
        if not room:
            raise HTTPException(
                status_code=404, detail=f"Record with {room_id} id does not exist"
            )
        try:
            update_room_data = room_data.model_dump(exclude_unset=True)
            return await self.repo.update(room, update_room_data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail="Room with this name already exist"
            )

    async def delete(self, room_id: int, delete_all: bool = False) -> int:
        try:
            return await self.repo.delete(room_id, delete_all)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=400, detail="Something went wrong. Try again"
            )
