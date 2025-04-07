from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.teacher import TeacherFromDB, TeacherToCreate
from app.api.dependecy import get_async_session, get_teacher_service
from app.services.teacher_service import TeacherService

router = APIRouter(prefix="/teacher", tags=["Teachers👨‍🎓"])


@router.get("/", response_model=list[TeacherFromDB])
async def get_all(
    service: TeacherService = Depends(get_teacher_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all(session=session)


@router.get("/{teacher_id}", response_model=TeacherFromDB)
async def get_one_by_id(
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_one_by_id(session=session, teacher_id=teacher_id)


@router.post("/", response_model=TeacherFromDB)
async def create(
    teacher_data: TeacherToCreate,
    service: TeacherService = Depends(get_teacher_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create(session=session, teacher_data=teacher_data)


@router.put("/{teacher_id}", response_model=TeacherFromDB)
async def update(
    teacher_id: int,
    update_data: TeacherToCreate,
    service: TeacherService = Depends(get_teacher_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.update(
        session=session, teacher_id=teacher_id, teacher_data=update_data
    )


@router.delete("/")
async def delete(
    teacher_id: int | None = None,
    delete_all: bool = False,
    service: TeacherService = Depends(get_teacher_service),
    session: AsyncSession = Depends(get_async_session),
):
    if not teacher_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(
        session=session, teacher_id=teacher_id, delete_all=delete_all
    )
