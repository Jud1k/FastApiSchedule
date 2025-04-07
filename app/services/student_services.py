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
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    async def get_all(self, session: AsyncSession) -> list[StudentFromDB]:
        async with session.begin():
            return await self.student_repo.get_all(session)

    async def get_one_by_id(
        self, session: AsyncSession, student_id: int
    ) -> StudentFromDB:
        async with session.begin():
            record = await self.student_repo.get_one_or_none_by_id(
                id=student_id, session=session
            )
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {student_id} id does not exist",
                )
            return record

    async def create(
        self, session: AsyncSession, student_data: StudentToCreate
    ) -> StudentFromDB:
        async with session.begin():
            data = student_data.model_dump()
            try:
                return await self.student_repo.create(data=data, session=session)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Student with this telephone number or email alredy exist",
                )

    async def update(
        self, session: AsyncSession, student_id: int, student_data: StudentToCreate
    ) -> StudentFromDB:
        async with session.begin():
            student = await self.student_repo.get_one_or_none_by_id(
                id=student_id, session=session
            )
            if not student:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {student_id} id does not exist",
                )
            try:
                update_student_data = student_data.model_dump(exclude_unset=True)
                return await self.student_repo.update(
                    obj=student, update_data=update_student_data, session=session
                )
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400,
                    detail="Student with this telephone number or email alredy exist",
                )

    async def delete(
        self, session: AsyncSession, student_id: int | None, delete_all: bool = False
    ) -> int:
        async with session.begin():
            try:
                return await self.student_repo.delete(
                    id=student_id, delete_all=delete_all, session=session
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )

    async def get_students_with_group_name(
        self, session: AsyncSession
    )-> list[StudentsWithGroupName]:
        async with session.begin():
            return await self.student_repo.get_students_with_group_names(session=session)

