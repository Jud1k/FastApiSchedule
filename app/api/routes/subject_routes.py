from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.api.dependecy import get_async_session, get_subject_service
from app.services.subject_service import SubjectService

router = APIRouter(prefix="/subject", tags=["Subjects💡"])


@router.get("/", response_model=list[SubjectFromDB])
async def get_all(
    service: SubjectService = Depends(get_subject_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all(session=session)


@router.get("/{subject_id}", response_model=SubjectFromDB)
async def get_one_by_id(
    subject_id: int,
    service: SubjectService = Depends(get_subject_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_one_by_id(session=session, subject_id=subject_id)


@router.post("/", response_model=SubjectFromDB)
async def create(
    subject: SubjectToCreate,
    service: SubjectService = Depends(get_subject_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create(session=session, subject_data=subject)


@router.put("/{subject_id}", response_model=SubjectFromDB)
async def update(
    subject_id: int,
    subject: SubjectToCreate,
    service: SubjectService = Depends(get_subject_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.update(
        session=session, subject_id=subject_id, subject_data=subject
    )


@router.delete("/")
async def delete(
    subject_id: int | None = None,
    delete_all: bool = False,
    service: SubjectService = Depends(get_subject_service),
    session: AsyncSession = Depends(get_async_session),
):
    if not subject_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(
        session=session, subject_id=subject_id, delete_all=delete_all
    )
