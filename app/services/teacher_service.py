import logging
from app.api.schemas.teacher import TeacherFromDB, TeacherToCreate
from app.repositories.repository import TeacherRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class TeacherService:
    def __init__(self, teacher_repo: TeacherRepository):
        self.teacher_repo = teacher_repo

    async def get_all(self, session: AsyncSession) -> list[TeacherFromDB]:
        async with session.begin():
            return await self.teacher_repo.get_all(session=session)

    async def get_one_by_id(
        self, session: AsyncSession, teacher_id: int
    ) -> TeacherFromDB:
        async with session.begin():
            record = await self.teacher_repo.get_one_or_none_by_id(
                id=teacher_id, session=session
            )
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {teacher_id} id does not exist",
                )
            return record

    async def create(
        self, session: AsyncSession, teacher_data: TeacherToCreate
    ) -> TeacherFromDB:
        async with session.begin():
            data = teacher_data.model_dump()
            try:
                return await self.teacher_repo.create(data=data, session=session)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Teacher with this telephone number or email alredy exist",
                )

    async def update(
        self,
        session: AsyncSession,
        teacher_id: int | None,
        teacher_data: TeacherToCreate,
    ) -> TeacherFromDB:
        async with session.begin():
            teacher = await self.teacher_repo.get_one_or_none_by_id(
                id=teacher_id, session=session
            )
            if not teacher:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {teacher_id} id does not exist",
                )
            try:
                update_teacher_data = teacher_data.model_dump(exclude_unset=True)
                return await self.teacher_repo.update(
                    obj=teacher, update_data=update_teacher_data, session=session
                )
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400,
                    detail="Teacher with this telephone number or email alredy exist",
                )

    async def delete(
        self, session: AsyncSession, teacher_id: int, delete_all: bool = False
    ) -> int:
        async with session.begin():
            try:
                return await self.teacher_repo.delete(
                    id=teacher_id, delete_all=delete_all, session=session
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )
