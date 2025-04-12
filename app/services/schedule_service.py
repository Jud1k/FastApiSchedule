from sqlite3 import IntegrityError
from fastapi import HTTPException
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.schedule import (
    ScheduleByGroupId,
    ScheduleFromDB,
    ScheduleToCreate,
    ScheduleWithNames,
)
from app.repositories.repository import ScheduleRepository


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository):
        self.schedule_repo = schedule_repo

    async def get_all(self, session: AsyncSession) -> list[ScheduleFromDB]:
        async with session.begin():
            return await self.schedule_repo.get_all(session=session)

    async def get_one_by_id(
        self, session: AsyncSession, schedule_id: int
    ) -> ScheduleFromDB:
        async with session.begin():
            record = await self.schedule_repo.get_one_or_none_by_id(
                session=session, id=schedule_id
            )
            if not record:
                raise HTTPException(
                    status_code=404,
                    detail=f"Record with {schedule_id} id does not exist",
                )
            return record

    async def create(
        self, session: AsyncSession, lesson_data: ScheduleToCreate
    ) -> ScheduleFromDB:
        async with session.begin():
            try:
                data = lesson_data.model_dump()
                return await self.schedule_repo.create(session=session, data=data)
            except IntegrityError as e:
                raise HTTPException(
                    status_code=400, detail="Invalid value for one of the arguments"
                )

    async def get_all_lessons_with_names(
        self, session: AsyncSession
    ) -> list[ScheduleWithNames]:
        async with session.begin():
            return await self.schedule_repo.get_all_lessons_with_names(session=session)

    async def get_all_lessons_with_names_by_group_id(
        self, group_id: int, session: AsyncSession
    ) -> list[ScheduleByGroupId]:
        async with session.begin():
            return await self.schedule_repo.get_all_lessons_wtih_names_by_group_id(
                group_id=group_id, session=session
            )
