from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.db.database import get_async_session
from app.services.group_service import GroupService

router = APIRouter(prefix="/group", tags=["Groups👩‍💻👨‍💻"])


async def get_group_service(session: AsyncSession = Depends(get_async_session)):
    return GroupService(session)


@router.get("/", response_model=list[GroupFromDB])
async def get_all(service: GroupService = Depends(get_group_service)):
    return await service.get_all()


@router.get("/{group_id}", response_model=GroupFromDB)
async def get_one_by_id(
    group_id: int, service: GroupService = Depends(get_group_service)
):
    return await service.get_one_by_id(group_id)


@router.post("/", response_model=GroupFromDB)
async def create(
    group: GroupToCreate, service: GroupService = Depends(get_group_service)
):
    return await service.create(group)


@router.put("/{group_id}", response_model=GroupFromDB)
async def update(
    group_id: int,
    group: GroupToCreate,
    service: GroupService = Depends(get_group_service),
):
    return await service.update(group_id, group)


@router.delete("/")
async def delete(
    group_id: int | None = None,
    delete_all: bool = False,
    service: GroupService = Depends(get_group_service),
):
    if not group_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(group_id, delete_all)
