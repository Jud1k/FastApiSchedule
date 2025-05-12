from fastapi import APIRouter, Depends
from app.api.dependencies.service_dep import get_schedule_service
from app.api.schemas.schedule import (
    ScheduleByGroupId,
    ScheduleFromDB,
    ScheduleToCreate,
    ScheduleWithNames,
)
from app.services.schedule_service import ScheduleService

router = APIRouter(prefix="/schedule", tags=["Schedule"])


@router.get("/", response_model=list[ScheduleFromDB])
async def get_schedule(
    service: ScheduleService = Depends(get_schedule_service)
):
    return await service.get_all()


@router.post("/", response_model=ScheduleFromDB)
async def create(
    lesson_data: ScheduleToCreate,
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.create(lesson_data=lesson_data)


@router.get("/lessons", response_model=list[ScheduleWithNames])
async def get_all_lessons_with_names(
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.get_all_lessons_with_names()


@router.get("/lessons/", response_model=list[ScheduleByGroupId])
async def get_all_lessons_with_names_by_group_id(
    group_id: int,
    service: ScheduleService = Depends(get_schedule_service),
):
    return await service.get_all_lessons_with_names_by_group_id(
        group_id=group_id,
    )
