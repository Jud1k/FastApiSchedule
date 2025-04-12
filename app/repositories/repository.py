from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.repositories.base_repository import SqlAlchemyRepository
from app.db.models import Student, Subject, Room, Teacher, Group, ScheduleLesson


class StudentRepository(SqlAlchemyRepository[Student]):
    model = Student

    async def get_students_with_group_names(self, session: AsyncSession) -> list[dict]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.group))
            .order_by(self.model.course)
        )
        result = await session.execute(stmt)
        students = result.scalars().all()
        return [
            {
                "id": student.id,
                "full_name": f"{student.first_name} {student.last_name}",
                "group_name": student.group.name if student.group else None,
                "course": student.course,
            }
            for student in students
        ]


class SubjectRepository(SqlAlchemyRepository[Subject]):
    model = Subject


class RoomRepository(SqlAlchemyRepository[Room]):
    model = Room


class TeacherRepository(SqlAlchemyRepository[Room]):
    model = Teacher


class GroupRepository(SqlAlchemyRepository[Group]):
    model = Group

    async def search_groups(self, session: AsyncSession, query: str) -> list[dict]:
        stmt = select(self.model).where(self.model.name.like("%" + query + "%"))
        result = await session.execute(stmt)
        groups = result.scalars().all()
        return groups


class ScheduleRepository(SqlAlchemyRepository[ScheduleLesson]):
    model = ScheduleLesson

    async def get_all_lessons_with_names(self, session: AsyncSession) -> list[dict]:
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

        result = await session.execute(stmt)
        lessons = result.scalars().all()
        return [
            {
                "id": lesson.id,
                "time_id": lesson.time_id,
                "day_week": lesson.day_week,
                "type_lesson": lesson.type_lesson,
                "group": lesson.group.name,
                "subject": lesson.subject.name,
                "teacher": f"{lesson.teacher.first_name} {lesson.teacher.last_name}",
                "room": lesson.room.name,
            }
            for lesson in lessons
        ]

    async def get_all_lessons_wtih_names_by_group_id(
        self, group_id: int, session: AsyncSession
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
        result = await session.execute(stmt)
        lessons = result.scalars().all()

        return (
            {
                "id": lesson.id,
                "time_id": lesson.time_id,
                "day_week": lesson.day_week,
                "type_lesson": lesson.type_lesson,
                "subject": lesson.subject.name,
                "teacher": f"{lesson.teacher.first_name} {lesson.teacher.last_name}",
                "room": lesson.room.name,
            }
            for lesson in lessons
        )
