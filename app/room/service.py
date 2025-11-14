import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictErr, NotFoundErr
from app.room.repository import RoomRepository
from app.room.schemas import RoomCreate, RoomUpdate
from app.shared.models import Room

logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, session: AsyncSession):
        self.room_repo = RoomRepository(session)

    async def get_all(self) -> list[Room]:
        return await self.room_repo.get_rooms()

    async def get_by_id(self, room_id: int) -> Room|None:
        room = await self.room_repo.get_room_by_id(room_id=room_id)
        return room

    async def create(self, room_in: RoomCreate) -> Room:
        try:
            return await self.room_repo.create(data=room_in)
        except IntegrityError as e:
            logger.error(f"Integirity error while creating room: {str(e)}")
            raise ConflictErr("Room")

    async def update(self, room_id: int, room_in: RoomUpdate) -> Room:
        room = await self.room_repo.get_one_or_none_by_id(id=room_id)
        if not room:
            logger.error(f"Room with {room_id} id does not exist")
            raise NotFoundErr("Group",room_id)
        try:
            return await self.room_repo.update(data=room, update_data=room_in)
        except IntegrityError as e:
            logger.error(f"Integirity error while updating room: {str(e)}")
            raise ConflictErr("Group")

    async def delete(self, room_id: int)->None:
        room = await self.room_repo.get_one_or_none_by_id(id=room_id)
        if not room:
            raise NotFoundErr("Room")
        return await self.room_repo.delete(id=room_id)

    async def search_rooms(self, query: str) -> list[Room]:
        return await self.room_repo.search(query=query)
