import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.domain.lesson.repository import LessonRepository
from app.domain.lesson.schemas import LessonCreate, LessonUpdate
from app.db.models import Lesson

logger = logging.getLogger(__name__)


class LessonService:
    def __init__(self, session: AsyncSession):
        self.lesson_repo = LessonRepository(session)

    async def get_all(self) -> list[Lesson]:
        return await self.lesson_repo.get_lessons()

    async def get_by_id(self, lesson_id: int) -> Lesson | None:
        lesson = await self.lesson_repo.get_one_or_none_by_id(id=lesson_id)
        return lesson

    async def get_lessons_by_group_id(self, group_id: int)->list[Lesson]:
        return await self.lesson_repo.get_lessons_by_group_id(group_id=group_id)

    async def get_lessons_by_room_id(self,room_id:int)->list[Lesson]:
        return await self.lesson_repo.get_lessons_by_room_id(room_id=room_id)
    
    async def get_lessons_by_teacher_id(self,teacher_id:int)->list[Lesson]:
        return await self.lesson_repo.get_lessons_by_teacher_id(teacher_id=teacher_id)
    
    async def create(self, lesson_in: LessonCreate) -> Lesson:
        try:
            lesson = await self.lesson_repo.create(data=lesson_in)
            return lesson
        except IntegrityError as e:
            logger.error(f"Integirity error while creating Lesson:{str(e)} ")
            raise ConflictException("Lesson")
        
    async def update(self, lesson_id: int, lesson_in: LessonUpdate) -> Lesson:
        lesson = await self.lesson_repo.get_one_or_none_by_id(id=lesson_id)
        if not lesson:
            raise NotFoundException("Lesson",lesson_id)
        try:
            return await self.lesson_repo.update(data=lesson, update_data=lesson_in)
        except IntegrityError as e:
            logger.error(f"Integirity error while updating Lesson: {str(e)}")
            raise ConflictException("Lesson")

    async def delete(self, lesson_id: int):
        lesson = await self.lesson_repo.get_one_or_none_by_id(id=lesson_id)
        if not lesson:
            raise NotFoundException("Lesson",lesson_id)
        return await self.lesson_repo.delete(id=lesson_id)
