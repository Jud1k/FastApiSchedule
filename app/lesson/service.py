import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictError, NotFoundError
from app.lesson.repository import LessonRepository
from app.lesson.schemas import LessonCreate, LessonUpdate
from app.shared.models import Lesson

logger = logging.getLogger(__name__)


class LessonService:
    def __init__(self, session: AsyncSession):
        self.lesson_repo = LessonRepository(session)

    async def get_all(self) -> list[Lesson]:
        return await self.lesson_repo.get_lessons()

    async def get_by_id(self, lesson_id: int) -> Lesson | None:
        lesson = await self.lesson_repo.get_one_or_none_by_id(id=lesson_id)
        if not lesson:
            raise HTTPException(
                status_code=404,
                detail=f"Record with {lesson_id} id does not exist",
            )
        return lesson

    async def get_lessons_by_group_id(self, group_id: int):
        return await self.lesson_repo.get_lessons_by_group_id(group_id=group_id)

    async def create(self, lesson_in: LessonCreate) -> Lesson:
        try:
            data = lesson_in.model_dump()
            return await self.lesson_repo.create(data=data)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid value for one of the arguments")

    async def update(self, lesson_id: int, lesson_in: LessonUpdate) -> Lesson:
        lesson = await self.lesson_repo.get_one_or_none_by_id(id=lesson_id)
        if not lesson:
            logger.error(f"Lesson with {lesson_id} does not exist")
            raise NotFoundError("An lesson with this id does not exist")
        try:
            update_data = lesson_in.model_dump(exclude_unset=True)
            return await self.lesson_repo.update(data=lesson, update_data=update_data)
        except IntegrityError as e:
            logger.error({e})
            raise ConflictError("An lesson with this name alredy exist")

    async def delete(self, lesson_id: int):
        try:
            return await self.lesson_repo.delete(id=lesson_id)
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail=str(e))
