import logging
from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.exceptions import ConflictError, NotFoundError
from app.repositories.repository import SubjectRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


class SubjectService:
    def __init__(self, session: AsyncSession):
        self.subject_repo = SubjectRepository(session)

    async def get_all(self) -> list[SubjectFromDB]:
        return await self.subject_repo.get_all()

    async def get_one_by_id(self, subject_id: int) -> SubjectFromDB:
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        if not subject:
            logger.error(f"Subject with {subject_id} id does not exist")
            raise NotFoundError("An subject with this id does not exist")
        return subject

    async def create(self, subject_in: SubjectToCreate) -> SubjectFromDB:
        subject = await self.subject_repo.get_one_or_none(filters=subject_in)
        if subject:
            logger.error(f"Subject with {subject_in.name} name already exist")
            raise ConflictError("An subject with this name already exist")
        data = subject_in.model_dump()
        return await self.subject_repo.create(data=data)

    async def update(
        self,
        subject_id: int,
        subject_in: SubjectToCreate,
    ) -> SubjectFromDB:
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        if not subject:
            logger.error(f"Subject with {subject_id} id does not exist")
            raise NotFoundError("An subject with this id does not exist")
        try:
            update_data = subject_in.model_dump(exclude_unset=True)
            return await self.subject_repo.update(
                data=subject,
                update_data=update_data,
            )
        except IntegrityError as e:
            logger.error({e})
            raise ConflictError("Subject with this name alredy exist")

    async def delete(self, subject_id: int):
        subject = await self.subject_repo.get_one_or_none_by_id(id=subject_id)
        if not subject:
            logger.error(f"Subject with {subject_id} id does not exist")
            raise NotFoundError("An subject with this id does not exist")
        return await self.subject_repo.delete(id=subject_id)

    async def search_subjects(self, query: str) -> list[SubjectFromDB]:
        return await self.subject_repo.search(query=query)
