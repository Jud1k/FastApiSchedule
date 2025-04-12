from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependecy import get_async_session, get_schedule_service
from app.api.schemas.schedule import (
    ScheduleByGroupId,
    ScheduleFromDB,
    ScheduleToCreate,
    ScheduleWithNames,
)
from app.services.schedule_service import ScheduleService

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.get("/", response_model=list[ScheduleFromDB])
async def get_all(
    session: AsyncSession = Depends(get_async_session),
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.get_all(session=session)


@router.post("/", response_model=ScheduleFromDB)
async def create(
    lesson_data: ScheduleToCreate,
    session: AsyncSession = Depends(get_async_session),
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.create(session=session, lesson_data=lesson_data)


@router.get("/lessons", response_model=list[ScheduleWithNames])
async def get_all_lessons_with_names(
    session: AsyncSession = Depends(get_async_session),
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.get_all_lessons_with_names(session=session)


@router.get("/lessons/", response_model=list[ScheduleByGroupId])
async def get_all_lessons_with_names_by_group_id(
    group_id:int,
    session: AsyncSession = Depends(get_async_session),
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.get_all_lessons_with_names_by_group_id(group_id=group_id,session=session)
