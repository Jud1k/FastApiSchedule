from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from app.api.schemas.teacher import TeacherFromDB, TeacherToCreate
from app.api.dependencies.service_dep import get_teacher_service
from app.exceptions import ConflictError, NotFoundError
from app.services.teacher_service import TeacherService

router = APIRouter(prefix="/teacher", tags=["Teachers👨‍🎓"])


@router.get("/search", response_model=list[TeacherFromDB])
async def search_teachers_by_name(
    query: str = Query(max_length=50),
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.search_teachers(query=query)


@router.get("/", response_model=list[TeacherFromDB])
async def get_all(
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.get_all()


@router.get("/{teacher_id}", response_model=TeacherFromDB)
async def get_one_by_id(
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.get_one_by_id(teacher_id=teacher_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=TeacherFromDB)
async def create(
    teacher_in: TeacherToCreate,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.create(teacher_in=teacher_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{teacher_id}", response_model=TeacherFromDB)
async def update(
    teacher_id: int,
    teacher_in: TeacherToCreate,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.update(teacher_id=teacher_id, teacher_in=teacher_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{teacher_id}")
async def delete(
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.delete(teacher_id=teacher_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
