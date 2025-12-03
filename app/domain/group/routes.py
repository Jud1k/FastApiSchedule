from fastapi import APIRouter, Depends, status
from fastapi.params import Query

from app.core.deps.auth import get_current_admin_user
from app.core.deps.service import GroupServiceDep
from app.exceptions import NotFoundException
from app.domain.group.schemas import GroupRead, GroupSummary, GroupCreate, GroupUpdate

router = APIRouter(prefix="/group", tags=["Groups👩‍💻👨‍💻"],dependencies=[Depends(get_current_admin_user)])


@router.get("/search", response_model=list[GroupRead])
async def search_groups_by_name(
    service: GroupServiceDep,
    query = Query(max_length=50),
):
    return await service.search_groups(query=str(query))


@router.get("/summary/", response_model=list[GroupSummary])
async def get_groups_summary(service: GroupServiceDep):
    return await service.get_groups_summary()


@router.get("/", response_model=list[GroupRead])
async def get_all_groups(
    service: GroupServiceDep
):
    return await service.get_all()


@router.get("/{group_id}", response_model=GroupRead)
async def get_group_by_id(
    group_id: int,
    service: GroupServiceDep
):
        group = await service.get_by_id(group_id=group_id)
        if not group:
            raise NotFoundException("Group",group_id)
        return group

@router.post("/", response_model=GroupRead,status_code=status.HTTP_201_CREATED)
async def create_group(
    group_in: GroupCreate,
    service: GroupServiceDep
):
    return await service.create(group_in=group_in)



@router.put("/{group_id}", response_model=GroupRead)
async def update_group(
    group_id: int,
    group_in: GroupUpdate,
    service: GroupServiceDep
):
    return await service.update(group_id=group_id, group_in=group_in)


@router.delete("/{group_id}", response_model=None,status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    service: GroupServiceDep
):
    await service.delete(group_id=group_id)

