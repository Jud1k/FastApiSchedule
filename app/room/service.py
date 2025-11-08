import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictError, NotFoundError
from app.room.repository import RoomRepository
from app.room.schemas import RoomCreate, RoomUpdate
from app.shared.models import Room

logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, session: AsyncSession):
        self.room_repo = RoomRepository(session)

    async def get_all(self) -> list[Room]:
        return await self.room_repo.get_rooms()

    async def get_by_id(self, room_id: int) -> Room:
        room = await self.room_repo.get_one_or_none_by_id(id=room_id)
        if not room:
            logger.error(f"Room with {room_id} id does not exist")
            raise NotFoundError("A room with this id does not exist")
        return room

    async def create(self, room_in: RoomCreate) -> Room:
        data = room_in.model_dump()
        try:
            return await self.room_repo.create(data=data)
        except IntegrityError as e:
            raise ConflictError(str(e))

    async def update(self, room_id: int, room_in: RoomUpdate) -> Room:
        room = await self.room_repo.get_one_or_none_by_id(id=room_id)
        if not room:
            logger.error(f"Room with {room_id} id does not exist")
            raise NotFoundError("An room with this id does not exist")
        try:
            update_data = room_in.model_dump(exclude_unset=True)
            return await self.room_repo.update(data=room, update_data=update_data)
        except IntegrityError as e:
            logger.error({e})
            raise ConflictError("An room with this name alredy exist")

    async def delete(self, room_id: int):
        room = await self.room_repo.get_one_or_none_by_id(id=room_id)
        if not room:
            logger.error(f"Room with {room_id} id does not exist")
            raise NotFoundError("An room with this id does not exist")
        return await self.room_repo.delete(id=room_id)

    async def search_rooms(self, query: str) -> list[Room]:
        return await self.room_repo.search(query=query)
