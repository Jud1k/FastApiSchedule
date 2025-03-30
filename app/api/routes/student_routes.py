from fastapi import APIRouter, Depends, status
from fastapi.exceptions import ResponseValidationError, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.student import StudentFromDB, StudentToCreate
from app.db.database import get_async_session
from app.services.student_services import StudentService

router = APIRouter(prefix="/student", tags=["Students🧑"])


async def get_student_service(session: AsyncSession = Depends(get_async_session)):
    return StudentService(session)


@router.get("/", response_model=list[StudentFromDB])
async def get_all(service: StudentService = Depends(get_student_service)):
    return await service.get_all()


@router.get("/{student_id}", response_model=StudentFromDB)
async def get_one_by_id(
    student_id: int, service: StudentService = Depends(get_student_service)
):
    return await service.get_one_by_id(student_id)


@router.post("/", response_model=StudentFromDB)
async def create(
    student_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.create(student_data)


@router.put("/{student_id}", response_model=StudentFromDB)
async def update(
    student_id: int,
    update_data: StudentToCreate,
    service: StudentService = Depends(get_student_service),
):
    return await service.update(student_id, update_data)


@router.delete("/")
async def delete(
    student_id: int | None = None,
    delete_all: bool = False,
    service: StudentService = Depends(get_student_service),
):
    if not student_id and not delete_all:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Need at least one argument")
    return await service.delete(student_id, delete_all)
