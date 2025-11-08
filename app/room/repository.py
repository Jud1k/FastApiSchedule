from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import Room


class RoomRepository(SqlAlchemyRepository[Room]):
    model = Room

    async def search(self, query: str) -> list[Room]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        rooms = results.scalars().all()
        return rooms

    async def get_rooms(self) -> list[Room]:
        stmt = select(self.model).options(joinedload(self.model.building))
        results = await self.session.execute(stmt)
        rooms = results.scalars().all()
        return rooms
