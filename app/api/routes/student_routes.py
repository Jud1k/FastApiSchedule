from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from app.api.schemas.student import (
    StudentFromDB,
    StudentToCreate,
    StudentsWithGroupName,
)
from app.api.dependencies.service_dep import get_student_service
from app.services.student_services import StudentService

router = APIRouter(prefix="/student", tags=["Students🧑"])


@router.get("/", response_model=list[StudentFromDB])
async def get_all_students(
    service: StudentService = Depends(get_student_service),
):
    return await service.get_all()


@router.get("/studentsandgroup", response_model=list[StudentsWithGroupName])
async def get_students_with_group_name(
    service: StudentService = Depends(get_student_service),
):
    return await service.get_students_with_group_name()


@router.get("/{student_id}", response_model=StudentFromDB)
async def get_student_by_id(
    student_id: int,
    service: StudentService = Depends(get_student_service),
):
    return await service.get_one_by_id(student_id=student_id)


@router.post("/", response_model=StudentFromDB)
async def create_student(
    student_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.create(student_data=student_data)


@router.put("/{student_id}", response_model=StudentFromDB)
async def update_student(
    student_id: int,
    update_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.update(student_id=student_id, student_data=update_data)


@router.delete("/")
async def delete_student(
    student_id: int | None = None,
    delete_all: bool = False,
    service: StudentService = Depends(get_student_service),
):
    if not student_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(student_id=student_id, delete_all=delete_all)
