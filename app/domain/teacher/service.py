import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.db.models import Teacher
from app.domain.teacher.repository import TeacherRepository
from app.domain.teacher.schemas import TeacherCreate, TeacherUpdate

logger = logging.getLogger(__name__)


class TeacherService:
    def __init__(self, session: AsyncSession):
        self.teacher_repo = TeacherRepository(session)

    async def get_all(self) -> list[Teacher]:
        return await self.teacher_repo.get_all()

    async def get_by_id(self, teacher_id: int) -> Teacher|None:
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        return teacher

    async def create(self, teacher_in: TeacherCreate) -> Teacher:
        try:        
            teacher = await self.teacher_repo.create(data=teacher_in)
            return teacher
        except IntegrityError as e:
            logger.error(f"Integirity error while creating teacher: {str(e)}")
            raise ConflictException("Teacher")
        
    async def update(
        self,
        teacher_id: int,
        teacher_in: TeacherUpdate,
    ) -> Teacher:
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        if not teacher:
            raise NotFoundException("Teacher",teacher_id)
        try:
            return await self.teacher_repo.update(data=teacher, update_data=teacher_in)
        except IntegrityError as e:
            logger.error(f"Integirity error while updating teacher: {str(e)}")
            raise ConflictException("Teacher")
        
    async def delete(self, teacher_id: int):
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        if not teacher:
            raise NotFoundException("Teacher",teacher_id)
        return await self.teacher_repo.delete(id=teacher_id)

    async def search_teachers(self, query: str) -> list[Teacher]:
        return await self.teacher_repo.search(query=query)
