import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.models import Student
from app.student.repository import StudentRepository
from app.student.schemas import StudentCreate, StudentUpdate

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self, session: AsyncSession):
        self.student_repo = StudentRepository(session)

    async def get_all(self) -> list[Student]:
        return await self.student_repo.get_students()

    async def get_by_id(self, student_id: int) -> Student:
        student = await self.student_repo.get_one_or_none_by_id(
            id=student_id,
        )
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Record with {student_id} id does not exist",
            )
        return student

    async def create(self, student_in: StudentCreate) -> Student:
        data = student_in.model_dump()
        try:
            return await self.student_repo.create(data=data)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Student with this telephone number or email alredy exist",
            )

    async def update(self, student_id: int, student_in: StudentUpdate) -> Student:
        student = await self.student_repo.get_one_or_none_by_id(
            id=student_id,
        )
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Record with {student_id} id does not exist",
            )
        try:
            update_data = student_in.model_dump(exclude_unset=True)
            return await self.student_repo.update(
                data=student,
                update_data=update_data,
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )

    async def delete(self, student_id: int):
        try:
            return await self.student_repo.delete(
                id=student_id,
            )
        except SQLAlchemyError:
            raise HTTPException(status_code=400, detail="Something went wrong. Try again")
