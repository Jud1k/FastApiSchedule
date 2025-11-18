import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ConflictException, NotFoundException
from app.db.models import Subject
from app.domain.subject.repository import SubjectRepository
from app.domain.subject.schemas import SubjectCreate, SubjectUpdate

logger = logging.getLogger(__name__)


class SubjectService:
    def __init__(self, session: AsyncSession):
        self.subject_repo = SubjectRepository(session)

    async def get_all(self) -> list[Subject]:
        return await self.subject_repo.get_all()

    async def get_by_id(self, subject_id: int) -> Subject|None:
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        return subject

    async def create(self, subject_in: SubjectCreate) -> Subject:
        logger.error(f"Subject with {subject_in.name} name already exist")
        try:
            subject = await self.subject_repo.create(data=subject_in)
            return subject
        except IntegrityError as e:
            logger.error(f"Integirity error while creating subject: {str(e)}")
            raise ConflictException("Subject")
        
    async def update(
        self,
        subject_id: int,
        subject_in: SubjectUpdate,
    ) -> Subject:
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        if not subject:
            raise NotFoundException("Subject",subject_id)
        try:
            return await self.subject_repo.update(
                data=subject,
                update_data=subject_in,
            )
        except IntegrityError as e:
            logger.error(f"Integirity error while updating subject: {str(e)}")
            raise ConflictException("Subject")

    async def delete(self, subject_id: int)->None:
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        if not subject:
            raise NotFoundException("Subject",subject_id)
        return await self.subject_repo.delete(id=subject_id)

    async def search_subjects(self, query: str) -> list[Subject]:
        return await self.subject_repo.search(query=query)
