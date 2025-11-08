from sqlalchemy import select

from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import Teacher


class TeacherRepository(SqlAlchemyRepository[Teacher]):
    model = Teacher

    async def search(self, query: str) -> list[Teacher]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        teachers = results.scalars().all()
        return teachers
