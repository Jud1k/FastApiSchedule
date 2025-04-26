import logging
from app.api.schemas.student import (
    StudentFromDB,
    StudentToCreate,
    StudentsWithGroupName,
)
from app.repositories.repository import StudentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self,session:AsyncSession):
        self.student_repo = StudentRepository(session)

    async def get_all(self) -> list[StudentFromDB]:
            return await self.student_repo.get_all()

    async def get_one_by_id(
        self, student_id: int
    ) -> StudentFromDB:
            record = await self.student_repo.get_one_or_none_by_id(
                id=student_id, 
            )
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {student_id} id does not exist",
                )
            return record

    async def create(
        self, student_data: StudentToCreate
    ) -> StudentFromDB:
            data = student_data.model_dump()
            try:
                return await self.student_repo.create(data=data)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Student with this telephone number or email alredy exist",
                )

    async def update(
        self, student_id: int, student_data: StudentToCreate
    ) -> StudentFromDB:
            student = await self.student_repo.get_one_or_none_by_id(
                id=student_id, 
            )
            if not student:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {student_id} id does not exist",
                )
            try:
                update_student_data = student_data.model_dump(exclude_unset=True)
                return await self.student_repo.update(
                    obj=student, update_data=update_student_data, 
                )
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400,
                    detail="Student with this telephone number or email alredy exist",
                )

    async def delete(
        self, student_id: int | None, delete_all: bool = False
    ) -> int:
            try:
                return await self.student_repo.delete(
                    id=student_id, delete_all=delete_all, 
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )

    async def get_students_with_group_name(
        self
    )-> list[StudentsWithGroupName]:
            return await self.student_repo.get_students_with_group_names()

