from fastapi import APIRouter,status

from app.core.deps.service import StudentServiceDep
from app.exceptions import NotFoundException
from app.domain.student.schemas import (
    StudentCreate,
    StudentRead,
    StudentUpdate,
)

router = APIRouter(prefix="/student", tags=["Students🧑"])


@router.get("/", response_model=list[StudentRead])
async def get_all_students(
    service:StudentServiceDep
):
    return await service.get_all()


@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id(
    student_id: int,
    service:StudentServiceDep
):
    student =  await service.get_by_id(student_id=student_id)
    if not student:
        raise NotFoundException("Student",student_id)

@router.post("/", response_model=StudentRead,status_code=status.HTTP_201_CREATED)
async def create_student(
    student_in: StudentCreate,
    service:StudentServiceDep
):
    return await service.create(student_in=student_in)


@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    service:StudentServiceDep
):
    return await service.update(student_id=student_id, student_in=student_in)


@router.delete("/", response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    service:StudentServiceDep
):
    return await service.delete(student_id=student_id)
