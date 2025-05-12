import logging
from app.api.schemas.teacher import TeacherFromDB, TeacherToCreate
from app.exceptions import ConflictError, NotFoundError
from app.repositories.repository import TeacherRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


logger = logging.getLogger(__name__)


class TeacherService:
    def __init__(self, session: AsyncSession):
        self.teacher_repo = TeacherRepository(session)

    async def get_all(self) -> list[TeacherFromDB]:
        return await self.teacher_repo.get_all()

    async def get_one_by_id(self, teacher_id: int) -> TeacherFromDB:
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        if not teacher:
            logger.error(f"Teacher with {teacher_id} does not exist")
            raise NotFoundError("An teacher with this id does not exist")
        return teacher

    async def create(self, teacher_in: TeacherToCreate) -> TeacherFromDB:
        teacher = await self.teacher_repo.get_one_or_none(filters=teacher_in)
        if teacher:
            logger.error(f"Teacher with {teacher_in.name} name already exist")
            raise ConflictError("An teacher with this name already exist")
        data = teacher_in.model_dump()
        return await self.teacher_repo.create(data=data)

    async def update(
        self,
        teacher_id: int,
        teacher_in: TeacherToCreate,
    ) -> TeacherFromDB:
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        if not teacher:
            logger.error(f"Teacher with {teacher_id} id does not exist")
            raise NotFoundError("An teacher with this id does not exist")
        try:
            update_data = teacher_in.model_dump(exclude_unset=True)
            return await self.teacher_repo.update(
                data=teacher, update_data=update_data
            )
        except IntegrityError as e:
            logger.error({e})
            raise ConflictError("An teacher with this name already exist")

    async def delete(self, teacher_id: int):
        teacher = await self.teacher_repo.get_one_or_none_by_id(id=teacher_id)
        if not teacher:
            logger.error(f"Teacher with {teacher_id} does not exist")
            raise NotFoundError("An teacher with this id does not exist")
        return await self.teacher_repo.delete(id=teacher_id)

    async def search_teachers(self, query: str) -> list[TeacherFromDB]:
        return await self.teacher_repo.search(query=query)
