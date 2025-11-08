from fastapi import APIRouter, Depends

from app.core.deps.service import get_student_service
from app.student.schemas import (
    StudentCreate,
    StudentRead,
    StudentUpdate,
)
from app.student.service import StudentService

router = APIRouter(prefix="/student", tags=["Students🧑"])


@router.get("/", response_model=list[StudentRead])
async def get_all_students(
    service: StudentService = Depends(get_student_service),
):
    return await service.get_all()


@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    return await service.get_by_id(student_id=student_id)


@router.post("/", response_model=StudentRead)
async def create_student(
    student_in: StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.create(student_in=student_in)


@router.put("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    service: StudentService = Depends(get_student_service),
):
    return await service.update(student_id=student_id, student_in=student_in)


@router.delete("/", response_model=None)
async def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    return await service.delete(student_id=student_id)
