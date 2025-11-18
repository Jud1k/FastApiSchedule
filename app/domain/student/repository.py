from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Student


class StudentRepository(SqlAlchemyRepository[Student]):
    model = Student

    async def get_students(self) -> list[Student]:
        stmt = select(self.model).options(joinedload(self.model.group))
        result = await self.session.execute(stmt)
        students = list(result.scalars().all())
        return students
