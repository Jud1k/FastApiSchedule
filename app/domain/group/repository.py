from sqlalchemy import func, select

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Group, Student


class GroupRepository(SqlAlchemyRepository[Group]):
    model = Group

    async def search(self, query: str) -> list[Group]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        groups = list(results.scalars().all())
        return groups

    async def get_groups_summary(self):
        stmt = (
            select(
                self.model.id,
                self.model.name,
                self.model.course,
                self.model.institute,
                func.count(Student.id).label("count_students"),
            )
            .outerjoin(self.model.students)
            .group_by(self.model.id)
        )
        results = await self.session.execute(stmt)
        groups = results.mappings().all()
        return groups
