from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import Lesson


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
            .order_by(self.model.day_week)
        )

        result = await self.session.execute(stmt)
        lessons = list(result.scalars().all())
        return lessons

    async def get_lessons_by_group_id(
        self,
        group_id: int,
    ) -> list[dict]:
        stmt = (
            select(self.model)
            .options(
                joinedload(self.model.subject),
                joinedload(self.model.room),
                joinedload(self.model.teacher),
            )
            .where(self.model.group_id == group_id)
            .order_by(self.model.day_week)
        )
        result = await self.session.execute(stmt)
        lessons = result.scalars().all()

        return (
            {
                "id": lesson.id,
                "time_id": lesson.time_id,
                "day_week": lesson.day_week,
                "type_lesson": lesson.type_lesson,
                "subject": lesson.subject.name,
                "teacher": lesson.teacher.name,
                "room": lesson.room.name,
            }
            for lesson in lessons
        )
