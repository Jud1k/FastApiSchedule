from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.db.database import get_async_session
from app.services.subject_service import SubjectService

router = APIRouter(prefix="/subject", tags=["Subjects💡"])


async def get_subject_service(session: AsyncSession = Depends(get_async_session)):
    return SubjectService(session)


@router.get("/", response_model=list[SubjectFromDB])
async def get_all(service: SubjectService = Depends(get_subject_service)):
    return await service.get_all()


@router.get("/{subject_id}", response_model=SubjectFromDB)
async def get_one_by_id(
    subject_id: int, service: SubjectService = Depends(get_subject_service)
):
    return await service.get_one_by_id(subject_id)


@router.post("/", response_model=SubjectFromDB)
async def create(
    subject: SubjectToCreate, service: SubjectService = Depends(get_subject_service)
):
    return await service.create(subject)


@router.put("/{subject_id}", response_model=SubjectFromDB)
async def update(
    subject_id: int,
    subject: SubjectToCreate,
    service: SubjectService = Depends(get_subject_service),
):
    return await service.update(subject_id, subject)


@router.delete("/")
async def delete(
    subject_id: int | None = None,
    delete_all: bool = False,
    service: SubjectService = Depends(get_subject_service),
):
    if not subject_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(subject_id, delete_all)
