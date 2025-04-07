import logging
from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.repositories.repository import SubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class SubjectService:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    async def get_all(self, session: AsyncSession) -> list[SubjectFromDB]:
        async with session.begin():
            return await self.subject_repo.get_all(session)

    async def get_one_by_id(
        self, session: AsyncSession, subject_id: int
    ) -> SubjectFromDB:
        async with session.begin():
            record = await self.subject_repo.get_one_or_none_by_id(
                id=subject_id, session=session
            )
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {subject_id} id does not exist",
                )
            return record

    async def create(
        self, session: AsyncSession, subject_data: SubjectToCreate
    ) -> SubjectFromDB:
        async with session.begin():
            data = subject_data.model_dump()
            try:
                return await self.subject_repo.create(data=data, session=session)
            except IntegrityError:
                raise HTTPException(
                    status_code=400,
                    detail="Subject with this name alredy exist",
                )

    async def update(
        self,
        session: AsyncSession,
        subject_id: int | None,
        subject_data: SubjectToCreate,
    ) -> SubjectFromDB:
        async with session.begin():
            subject = await self.subject_repo.get_one_or_none_by_id(
                id=subject_id, session=session
            )
            if not subject:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {subject_id} id does not exist",
                )
            try:
                update_subject_data = subject_data.model_dump(exclude_unset=True)
                return await self.subject_repo.update(
                    obj=subject, update_data=update_subject_data, session=session
                )
            except IntegrityError:
                raise HTTPException(
                    status_code=400, detail="Subject with this name alredy exist"
                )

    async def delete(
        self, session: AsyncSession, subject_id: int, delete_all: bool = False
    ) -> int:
        async with session.begin():
            try:
                return await self.subject_repo.delete(
                    id=subject_id, delete_all=delete_all, session=session
                )
            except SQLAlchemyError:
                raise HTTPException(
                    status_code=400, detail="Something went wrong. Try again"
                )
