from fastapi import APIRouter, status
from fastapi.params import Query

from app.core.deps.service import SubjectServiceDep
from app.exceptions import NotFoundException
from app.domain.subject.schemas import SubjectRead, SubjectCreate, SubjectUpdate

router = APIRouter(prefix="/subject", tags=["Subjects💡"])


@router.get("/search", response_model=list[SubjectRead])
async def search_subject_by_name(
    service: SubjectServiceDep,
    query = Query(max_length=50),
):
    return await service.search_subjects(query=str(query))


@router.get("/", response_model=list[SubjectRead])
async def get_all(
    service: SubjectServiceDep
):
    return await service.get_all()


@router.get("/{subject_id}", response_model=SubjectRead)
async def get_one_by_id(
    subject_id: int,
    service: SubjectServiceDep
):
    subject = await service.get_by_id(subject_id=subject_id)
    if not subject:
        raise NotFoundException("Subject",subject_id)
    return subject

@router.post("/", response_model=SubjectRead,status_code=status.HTTP_201_CREATED)
async def create(
    subject_in: SubjectCreate,
    service: SubjectServiceDep
):
    return await service.create(subject_in=subject_in)



@router.put("/{subject_id}", response_model=SubjectRead)
async def update(
    subject_id: int,
    subject_in: SubjectUpdate,
    service: SubjectServiceDep
):
    return await service.update(subject_id=subject_id, subject_in=subject_in)



@router.delete("/{subject_id}", response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    subject_id: int,
    service: SubjectServiceDep
):
    return await service.delete(subject_id=subject_id)
