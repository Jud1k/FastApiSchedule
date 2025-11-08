from sqlalchemy import select

from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import Subject


class SubjectRepository(SqlAlchemyRepository[Subject]):
    model = Subject

    async def search(self, query: str) -> list[Subject]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        subjects = results.scalars().all()
        return subjects
