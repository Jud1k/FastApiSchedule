from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from app.api.schemas.subject import SubjectFromDB, SubjectToCreate
from app.api.dependencies.service_dep import get_subject_service
from app.exceptions import ConflictError, NotFoundError
from app.services.subject_service import SubjectService

router = APIRouter(prefix="/subject", tags=["Subjects💡"])


@router.get("/search", response_model=list[SubjectFromDB])
async def search_subject_by_name(
    query: str = Query(max_length=50),
    service: SubjectService = Depends(get_subject_service),
):
    return await service.search_subjects(query=query)


@router.get("/", response_model=list[SubjectFromDB])
async def get_all(
    service: SubjectService = Depends(get_subject_service),
):
    return await service.get_all()


@router.get("/{subject_id}", response_model=SubjectFromDB)
async def get_one_by_id(
    subject_id: int,
    service: SubjectService = Depends(get_subject_service),
):
    try:
        return await service.get_one_by_id(subject_id=subject_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=SubjectFromDB)
async def create(
    subject_in: SubjectToCreate,
    service: SubjectService = Depends(get_subject_service),
):
    try:
        return await service.create(subject_in=subject_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{subject_id}", response_model=SubjectFromDB)
async def update(
    subject_id: int,
    subject_in: SubjectToCreate,
    service: SubjectService = Depends(get_subject_service),
):
    try:
        return await service.update(subject_id=subject_id, subject_in=subject_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{subject_id}")
async def delete(
    subject_id: int,
    service: SubjectService = Depends(get_subject_service),
):
    try:
        return await service.delete(subject_id=subject_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
