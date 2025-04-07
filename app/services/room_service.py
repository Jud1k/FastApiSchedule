import logging
from app.api.schemas.room import RoomFromDB, RoomToCreate
from app.repositories.repository import RoomRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class RoomService:
    def __init__(self, room_repo: RoomRepository):
        self.room_repo = room_repo

    async def get_all(self, session: AsyncSession) -> list[RoomFromDB]:
        async with session.begin():
            return await self.room_repo.get_all(session)

    async def get_one_by_id(self, session: AsyncSession, room_id: int) -> RoomFromDB:
        async with session.begin():
            record = await self.room_repo.get_one_or_none_by_id(
                session=session, id=room_id
            )
            if not record:
                raise HTTPException(
                    status_code=404, detail=f"Record with {room_id} id does not exist"
                )
            return record

    async def create(
        self, session: AsyncSession, room_data: RoomToCreate
    ) -> RoomFromDB:
        async with session.begin():
            data = room_data.model_dump()
            try:
                return await self.room_repo.create(session=session, data=data)
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400,
                    detail="Room with this name alredy exist",
                )

    async def update(
        self, session: AsyncSession, room_id: int | None, room_data: RoomToCreate
    ) -> RoomFromDB:
        async with session.begin():
            room = await self.room_repo.get_one_or_none_by_id(
                session=session, id=room_id
            )
            if not room:
                raise HTTPException(
                    status_code=404, detail=f"Record with {room_id} id does not exist"
                )
            try:
                update_room_data = room_data.model_dump(exclude_unset=True)
                return await self.room_repo.update(
                    session=session, obj=room, update_data=update_room_data
                )
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400, detail="Room with this name already exist"
                )

    async def delete(
        self, session: AsyncSession, room_id: int | None, delete_all: bool = False
    ) -> int:
        async with session.begin():
            try:
                return await self.room_repo.delete(
                    session=session, id=room_id, delete_all=delete_all
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )
