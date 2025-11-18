from sqlalchemy import select

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Teacher


class TeacherRepository(SqlAlchemyRepository[Teacher]):
    model = Teacher

    async def search(self, query: str) -> list[Teacher]:
        stmt = select(self.model).where(self.model.first_name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        teachers = list(results.scalars().all())
        return teachers
