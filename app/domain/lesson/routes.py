from fastapi import APIRouter, HTTPException, status

from app.core.deps.service import LessonServiceDep
from app.domain.lesson.schemas import LessonCreate, LessonUpdate, LessonById, LessonReadMinimal

router = APIRouter(prefix="/lesson", tags=["Lessons"])


# @router.get("/", response_model=list[LessonRead])
# async def get_schedule(service: LessonService = Depends(get_lesson_service)):
#     return await service.get_all()


# @router.get("/{group_id}", response_model=list[LessonById])
# async def get_all_lessons_with_names_by_group_id(
#     group_id: int,
#     service: LessonServiceDep
# ):
#     return await service.get_lessons_by_group_id(
#         group_id=group_id,
#     )
    
@router.get("/",response_model=list[LessonById])
async def get_all_lessons_by_query(
    service: LessonServiceDep,
    group: int|None=None,
    teacher:int|None=None,
    room:int|None=None,
):
    filters_count = sum([bool(group), bool(teacher), bool(room)])
    
    if filters_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one filter is required")
    if filters_count > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only one filter parameter is allowed")
    if group:
        return await service.get_lessons_by_group_id(group_id=group)
    if teacher:
        return await service.get_lessons_by_teacher_id(teacher_id=teacher)
    if room:
        return await service.get_lessons_by_room_id(room_id=room)


@router.post("/", response_model=LessonReadMinimal,status_code=201)
async def create(
    lesson_in: LessonCreate,
    service: LessonServiceDep
):
    return await service.create(lesson_in=lesson_in)


@router.put("/{lesson_id}", response_model=LessonReadMinimal)
async def update_lesson(
    lesson_id: int,
    lesson_in: LessonUpdate,
    service: LessonServiceDep
):
    return await service.update(lesson_id=lesson_id, lesson_in=lesson_in)


@router.delete("/{lesson_id}", response_model=None,status_code=204)
async def delete_lesson(lesson_id: int, service:LessonServiceDep):
    return await service.delete(lesson_id=lesson_id)
