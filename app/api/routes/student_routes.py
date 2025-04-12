from fastapi import APIRouter, Depends, status
from fastapi.exceptions import ResponseValidationError, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.student import (
    StudentFromDB,
    StudentToCreate,
    StudentsWithGroupName,
)
from app.api.dependecy import get_async_session, get_student_service
from app.services.student_services import StudentService

router = APIRouter(prefix="/student", tags=["Students🧑"])


@router.get("/", response_model=list[StudentFromDB])
async def get_all(
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all(session=session)


@router.get("/student/{student_id}", response_model=StudentFromDB)
async def get_one_by_id(
    student_id: int,
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_one_by_id(session=session, student_id=student_id)


@router.post("/", response_model=StudentFromDB)
async def create(
    student_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create(session=session, student_data=student_data)


@router.put("/{student_id}", response_model=StudentFromDB)
async def update(
    student_id: int,
    update_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.update(
        session=session, student_id=student_id, student_data=update_data
    )


@router.delete("/")
async def delete(
    student_id: int | None = None,
    delete_all: bool = False,
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    if not student_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(
        session=session, student_id=student_id, delete_all=delete_all
    )


@router.get("/studentsandgroup", response_model=list[StudentsWithGroupName])
async def get_students_with_group_name(
    service: StudentService = Depends(get_student_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_students_with_group_name(session=session)
