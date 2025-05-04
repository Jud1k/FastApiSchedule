from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from app.api.schemas.group import GroupFromDB, GroupToCreate
from app.exceptions import ConflictError, NotFoundError
from app.services.group_service import GroupService
from app.api.dependecy import get_group_service

router = APIRouter(prefix="/group", tags=["Groups👩‍💻👨‍💻"])


@router.get("/search", response_model=list[GroupFromDB])
async def search_groups_by_name(
    query: str = Query(max_length=50),
    service: GroupService = Depends(get_group_service),
):
    return await service.search_groups(query=query)


@router.get("/", response_model=list[GroupFromDB])
async def get_all_groups(
    service: GroupService = Depends(get_group_service),
):
    return await service.get_all()


@router.get("/{group_id}", response_model=GroupFromDB)
async def get_group_by_id(
    group_id: int,
    service: GroupService = Depends(get_group_service),
):
    try:
        return await service.get_one_by_id(group_id=group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=GroupFromDB)
async def create_group(
    group_in: GroupToCreate,
    service: GroupService = Depends(get_group_service),
):
    try:
        return await service.create(group_in=group_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{group_id}", response_model=GroupFromDB)
async def update_group(
    group_id: int,
    group_in: GroupToCreate,
    service: GroupService = Depends(get_group_service),
):
    try:
        return await service.update(group_id=group_id, group_in=group_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    service: GroupService = Depends(get_group_service),
):
    try:
        await service.delete(group_id=group_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
