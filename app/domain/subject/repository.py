from sqlalchemy import select

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Subject


class SubjectRepository(SqlAlchemyRepository[Subject]):
    model = Subject

    async def search(self, query: str) -> list[Subject]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        subjects = list(results.scalars().all())
        return subjects
