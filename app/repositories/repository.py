from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.repositories.base_repository import SqlAlchemyRepository
from app.db.models import Student, Subject, Room, Teacher, Group, ScheduleLesson


class StudentRepository(SqlAlchemyRepository[Student]):
    model = Student

    async def get_students_with_group_names(self) -> list[dict]:
        stmt = (
            select(self.model)
            .options(joinedload(self.model.group))
            .order_by(self.model.course)
        )
        result = await self.session.execute(stmt)
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

    async def search_by_name(self, query: str) -> list[Subject]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        subjects = results.scalars().all()
        return subjects


class RoomRepository(SqlAlchemyRepository[Room]):
    model = Room

    async def search_by_name(self, query: str) -> list[Room]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        rooms = results.scalars().all()
        return rooms


class TeacherRepository(SqlAlchemyRepository[Teacher]):
    model = Teacher

    async def search_by_name(self, query: str) -> list[Teacher]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        teachers = results.scalars().all()
        return teachers


class GroupRepository(SqlAlchemyRepository[Group]):
    model = Group

    async def search_by_name(self, query: str) -> list[Group]:
        stmt = select(self.model).where(self.model.name.ilike(f"%{query}%"))
        results = await self.session.execute(stmt)
        groups = results.scalars().all()
        return groups


class ScheduleRepository(SqlAlchemyRepository[ScheduleLesson]):
    model = ScheduleLesson

    async def get_all_lessons_with_names(self) -> list[dict]:
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
        lessons = result.scalars().all()
        return [
            {
                "id": lesson.id,
                "time_id": lesson.time_id,
                "day_week": lesson.day_week,
                "type_lesson": lesson.type_lesson,
                "group": lesson.group.name,
                "subject": lesson.subject.name,
                "teacher": f"{lesson.teacher.name}",
                "room": lesson.room.name,
            }
            for lesson in lessons
        ]

    async def get_all_lessons_wtih_names_by_group_id(
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
                "teacher": {lesson.teacher.name},
                "room": lesson.room.name,
            }
            for lesson in lessons
        )
