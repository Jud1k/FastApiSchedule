from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.services.group_service import GroupService
from app.api.dependecy import get_async_session, get_group_service

router = APIRouter(prefix="/group", tags=["Groups👩‍💻👨‍💻"])


@router.get("/", response_model=list[GroupFromDB])
async def get_all(
    service: GroupService = Depends(get_group_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_all(session=session)


@router.get("/smthg/{group_id}", response_model=GroupFromDB)
async def get_one_by_id(
    group_id: int,
    service: GroupService = Depends(get_group_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_one_by_id(session=session, group_id=group_id)


@router.post("/", response_model=GroupFromDB)
async def create(
    group: GroupToCreate,
    service: GroupService = Depends(get_group_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.create(session=session, group_data=group)


@router.put("/{group_id}", response_model=GroupFromDB)
async def update(
    group_id: int,
    group: GroupToCreate,
    service: GroupService = Depends(get_group_service),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.update(session=session, group_id=group_id, group_data=group)


@router.delete("/")
async def delete(
    group_id: int | None = None,
    delete_all: bool = False,
    service: GroupService = Depends(get_group_service),
    session: AsyncSession = Depends(get_async_session),
):
    if not group_id and not delete_all:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Need at least one argument"
        )
    return await service.delete(
        session=session, group_id=group_id, delete_all=delete_all
    )


@router.get("/search")
async def search_groups(
    query:str=Query(default="ИЦЭ-21"),
    session: AsyncSession = Depends(get_async_session),
    service: GroupService = Depends(get_group_service),
):
    return await service.search_groups(session=session,query=query)
