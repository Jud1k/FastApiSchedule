from sqlite3 import IntegrityError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.schedule import (
    ScheduleByGroupId,
    ScheduleFromDB,
    ScheduleToCreate,
    ScheduleWithNames,
)
from app.repositories.repository import ScheduleRepository


class ScheduleService:
    def __init__(self, session: AsyncSession):
        self.schedule_repo = ScheduleRepository(session)

    async def get_all(self) -> list[ScheduleFromDB]:
        return await self.schedule_repo.get_all()

    async def get_one_by_id(self, schedule_id: int) -> ScheduleFromDB:
        record = await self.schedule_repo.get_one_or_none_by_id(id=schedule_id)
        if not record:
            raise HTTPException(
                status_code=404,
                detail=f"Record with {schedule_id} id does not exist",
            )
        return record

    async def create(self, lesson_data: ScheduleToCreate) -> ScheduleFromDB:
        try:
            data = lesson_data.model_dump()
            return await self.schedule_repo.create(data=data)
        except IntegrityError as e:
            raise HTTPException(
                status_code=400, detail="Invalid value for one of the arguments"
            )

    async def get_all_lessons_with_names(self) -> list[ScheduleWithNames]:
        return await self.schedule_repo.get_all_lessons_with_names()

    async def get_all_lessons_with_names_by_group_id(
        self, group_id: int
    ) -> list[ScheduleByGroupId]:
        return await self.schedule_repo.get_all_lessons_wtih_names_by_group_id(
            group_id=group_id
        )
