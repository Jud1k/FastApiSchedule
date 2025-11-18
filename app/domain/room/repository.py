from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Room


class RoomRepository(SqlAlchemyRepository[Room]):
    model = Room

    async def search(self, query: str) -> list[Room]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        rooms = list(results.scalars().all())
        return rooms

    async def get_rooms(self) -> list[Room]:
        stmt = select(self.model).options(joinedload(self.model.building))
        results = await self.session.execute(stmt)
        rooms = list(results.scalars().all())
        return rooms

    async def get_room_by_id(self,room_id:int)->Room|None:
        stmt = select(self.model).options(joinedload(self.model.building)).filter(self.model.id==room_id)
        result = await self.session.execute(stmt)
        room = result.scalar_one_or_none()
        return room