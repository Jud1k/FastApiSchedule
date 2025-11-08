from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps.service import get_lesson_service
from app.exceptions import ConflictError, NotFoundError
from app.lesson.schemas import LessonRead, LessonCreate, LessonUpdate, LessonByGroupId
from app.lesson.service import LessonService

router = APIRouter(prefix="/lesson", tags=["Lessons"])


@router.get("/", response_model=list[LessonRead])
async def get_schedule(service: LessonService = Depends(get_lesson_service)):
    return await service.get_all()


@router.get("/{group_id}", response_model=list[LessonByGroupId])
async def get_all_lessons_with_names_by_group_id(
    group_id: int,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.get_lessons_by_group_id(
        group_id=group_id,
    )


@router.post("/", response_model=LessonRead)
async def create(
    lesson_in: LessonCreate,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.create(lesson_in=lesson_in)


@router.put("/{lesson_id}", response_model=LessonRead)
async def update_lesson(
    lesson_id: int,
    lesson_in: LessonUpdate,
    service: LessonService = Depends(get_lesson_service),
):
    try:
        return await service.update(lesson_id=lesson_id, lesson_in=lesson_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{lesson_id}", response_model=None)
async def delete_lesson(lesson_id: int, service: LessonService = Depends(get_lesson_service)):
    return await service.delete(lesson_id=lesson_id)
