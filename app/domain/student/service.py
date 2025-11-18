import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.db.models import Student
from app.domain.student.repository import StudentRepository
from app.domain.student.schemas import StudentCreate, StudentUpdate

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self, session: AsyncSession):
        self.student_repo = StudentRepository(session)

    async def get_all(self) -> list[Student]:
        return await self.student_repo.get_students()

    async def get_by_id(self, student_id: int) -> Student|None:
        student = await self.student_repo.get_one_or_none_by_id(
            id=student_id,
        )
        return student

    async def create(self, student_in: StudentCreate) -> Student:
        try:
            student = await self.student_repo.create(data=student_in)
            return student
        except IntegrityError as e:
            logger.error(f"Integirity error while creating student: {str(e)}")
            raise ConflictException("Student")

    async def update(self, student_id: int, student_in: StudentUpdate) -> Student:
        student = await self.student_repo.get_one_or_none_by_id(
            id=student_id,
        )
        if not student:
            raise NotFoundException("Student",student_id)
        try:
            student= await self.student_repo.update(
                data=student,
                update_data=student_in,
            )
            return student
        except IntegrityError as e:
            logger.error(f"Integirity error while updating student: {str(e)}")
            raise ConflictException("Student",student_id)

    async def delete(self, student_id: int)->None:
        student = await self.student_repo.get_one_or_none_by_id(id=student_id)
        if not student:
            raise NotFoundException("Student",student_id) 
        return await self.student_repo.delete(
                id=student_id,
            )