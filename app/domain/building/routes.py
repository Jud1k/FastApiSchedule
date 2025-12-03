from fastapi import APIRouter, status,Depends

from app.core.deps.auth import get_current_admin_user
from app.domain.building.schemas import BuildingCreate, BuildingRead, BuildingUpdate
from app.core.deps.service import BuildingServiceDep
from app.exceptions import NotFoundException


router = APIRouter(prefix="/building", tags=["Building"],dependencies=[Depends(get_current_admin_user)])


@router.get("/", response_model=list[BuildingRead])
async def get_all_buildings(service: BuildingServiceDep):
    return await service.get_all()


@router.get("/{building_id}", response_model=BuildingRead)
async def get_building_by_id(building_id: int, service: BuildingServiceDep):
    building = await service.get_by_id(building_id)
    if not building:
        raise NotFoundException("Building",building_id)
    return building


@router.post("/", response_model=BuildingRead,status_code=status.HTTP_201_CREATED)
async def create_building(building_in: BuildingCreate, service: BuildingServiceDep):
    return await service.create(building_in=building_in)


@router.put("/{building_id}", response_model=BuildingRead)
async def update_building(
    building_id: int,
    building_in: BuildingUpdate,
    service: BuildingServiceDep,
):
    return await service.update(building_id=building_id, building_in=building_in)


@router.delete("/{building_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(building_id: int, service: BuildingServiceDep):
    return await service.delete(building_id=building_id)
