from fastapi import APIRouter
from fastapi.params import Query

from app.core.deps.service import TeacherServiceDep
from app.exceptions import NotFoundException
from app.domain.teacher.schemas import TeacherRead, TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/teacher", tags=["Teachers👨‍🎓"])


@router.get("/search", response_model=list[TeacherRead])
async def search_teachers_by_name(
    service: TeacherServiceDep,
    query = Query(max_length=50),
):
    return await service.search_teachers(query=str(query))


@router.get("/", response_model=list[TeacherRead])
async def get_all(
    service: TeacherServiceDep
):
    return await service.get_all()


@router.get("/{teacher_id}", response_model=TeacherRead)
async def get_one_by_id(
    teacher_id: int,
    service: TeacherServiceDep
):
    teacher = await service.get_by_id(teacher_id=teacher_id)
    if not teacher:
        raise NotFoundException("Teacher",teacher_id)
    return teacher

@router.post("/", response_model=TeacherRead,status_code=201)
async def create(
    teacher_in: TeacherCreate,
    service: TeacherServiceDep
):
    return await service.create(teacher_in=teacher_in)


@router.put("/{teacher_id}", response_model=TeacherRead)
async def update(
    teacher_id: int,
    teacher_in: TeacherUpdate,
    service: TeacherServiceDep
):
    return await service.update(teacher_id=teacher_id, teacher_in=teacher_in)


@router.delete("/{teacher_id}", response_model=None,status_code=204)
async def delete(
    teacher_id: int,
    service: TeacherServiceDep
):
    return await service.delete(teacher_id=teacher_id)
