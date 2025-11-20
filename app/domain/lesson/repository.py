from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Lesson


class LessonRepository(SqlAlchemyRepository[Lesson]):
    model = Lesson

    async def get_lessons(self) -> list[Lesson]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.group),
                joinedload(self.model.room),
                joinedload(self.model.subject),
                joinedload(self.model.teacher),
            )
            .order_by(self.model.day_of_week)
        )

        result = await self.session.execute(stmt)
        lessons = list(result.scalars().all())
        return lessons

    async def get_lessons_by_group_id(
        self,
        group_id: int,
    )->list[Lesson]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.subject),
                joinedload(self.model.room),
                joinedload(self.model.teacher),
                joinedload(self.model.group)
            )
            .where(self.model.group_id == group_id)
        )
        result = await self.session.execute(stmt)
        lessons = list(result.scalars().all())

        return lessons
    
    async def get_lessons_by_room_id(self,room_id:int)->list[Lesson]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.subject),
                joinedload(self.model.room),
                joinedload(self.model.teacher),
                joinedload(self.model.group)
            )
            .where(self.model.room_id == room_id)
        )
        result = await self.session.execute(stmt)
        lessons = list(result.scalars().all())
        
        return lessons
    
    async def get_lessons_by_teacher_id(self,teacher_id:int)->list[Lesson]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.subject),
                joinedload(self.model.room),
                joinedload(self.model.teacher),
                joinedload(self.model.group)
            )
            .where(self.model.teacher_id == teacher_id)
        )
        result = await self.session.execute(stmt)
        lessons = list(result.scalars().all())
        
        return lessons