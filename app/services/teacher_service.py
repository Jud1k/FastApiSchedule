import logging
from app.api.schemas.teacher import TeacherFromDB, TeacherToCreate
from app.repositories.repository import TeacherRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class TeacherService:
    def __init__(self, session: AsyncSession):
        self.repo = TeacherRepository(session)

    async def get_all(self) -> list[TeacherFromDB]:
        return await self.repo.get_all()

    async def get_one_by_id(self, teacher_id: int) -> TeacherFromDB:
        record = await self.repo.get_one_or_none_by_id(teacher_id)
        if not record:
            raise HTTPException(
                status_code=404, detail=f"Record with {teacher_id} id does not exist"
            )
        return record

    async def create(self, teacher_data: TeacherToCreate) -> TeacherFromDB:
        data = teacher_data.model_dump()
        try:
            return await self.repo.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Teacher with this telephone number or email alredy exist",
            )

    async def update(
        self, teacher_id: int | None, teacher_data: TeacherToCreate
    ) -> TeacherFromDB:
        teacher = await self.repo.get_one_or_none_by_id(teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=404, detail=f"Record with {teacher_id} id does not exist"
            )
        try:
            update_teacher_data = teacher_data.model_dump(exclude_unset=True)
            return await self.repo.update(teacher, update_teacher_data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400,
                detail="Teacher with this telephone number or email alredy exist",
            )

    async def delete(self, teacher_id: int, delete_all: bool = False) -> int:
        try:
            return await self.repo.delete(teacher_id, delete_all)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=400, detail="Something went wrong. Try again"
            )
