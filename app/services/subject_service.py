import logging
from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.repositories.repository import SubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException


logger = logging.getLogger(__name__)


class SubjectService:
    def __init__(self, session: AsyncSession):
        self.repo = SubjectRepository(session)

    async def get_all(self) -> list[SubjectFromDB]:
        return await self.repo.get_all()

    async def get_one_by_id(self, subject_id: int) -> SubjectFromDB:
        record = await self.repo.get_one_or_none_by_id(subject_id)
        if not record:
            raise HTTPException(
                status_code=404, detail=f"Record with {subject_id} id does not exist"
            )
        return record

    async def create(self, subject_data: SubjectToCreate) -> SubjectFromDB:
        data = subject_data.model_dump()
        try:
            return await self.repo.create(data)
        except IntegrityError:
            raise HTTPException(
                status_code=400,
                detail="Subject with this name alredy exist",
            )

    async def update(
        self, subject_id: int | None, subject_data: SubjectToCreate
    ) -> SubjectFromDB:
        subject = await self.repo.get_one_or_none_by_id(subject_id)
        if not subject:
            raise HTTPException(
                status_code=404, detail=f"Record with {subject_id} id does not exist"
            )
        try:
            update_subject_data = subject_data.model_dump(exclude_unset=True)
            return await self.repo.update(subject, update_subject_data)
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Subject with this name alredy exist"
            )

    async def delete(self, subject_id: int, delete_all: bool = False) -> int:
        try:
            return await self.repo.delete(subject_id, delete_all)
        except SQLAlchemyError:
            raise HTTPException(
                status_code=400, detail="Something went wrong. Try again"
            )
