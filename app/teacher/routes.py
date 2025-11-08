from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from app.core.deps.service import get_teacher_service
from app.exceptions import ConflictError, NotFoundError
from app.teacher.schemas import TeacherRead, TeacherCreate, TeacherUpdate
from app.teacher.service import TeacherService

router = APIRouter(prefix="/teacher", tags=["Teachers👨‍🎓"])


@router.get("/search", response_model=list[TeacherRead])
async def search_teachers_by_name(
    query: str = Query(max_length=50),
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.search_teachers(query=query)


@router.get("/", response_model=list[TeacherRead])
async def get_all(
    service: TeacherService = Depends(get_teacher_service),
):
    return await service.get_all()


@router.get("/{teacher_id}", response_model=TeacherRead)
async def get_one_by_id(
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.get_by_id(teacher_id=teacher_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=TeacherRead)
async def create(
    teacher_in: TeacherCreate,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.create(teacher_in=teacher_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{teacher_id}", response_model=TeacherRead)
async def update(
    teacher_id: int,
    teacher_in: TeacherUpdate,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.update(teacher_id=teacher_id, teacher_in=teacher_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{teacher_id}", response_model=None)
async def delete(
    teacher_id: int,
    service: TeacherService = Depends(get_teacher_service),
):
    try:
        return await service.delete(teacher_id=teacher_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
