from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.building.schemas import BuildingCreate, BuildingRead
from app.building.service import BuildingService
from app.core.deps.service import get_building_service
from app.exceptions import ConflictError, NotFoundError


router = APIRouter(prefix="/building", tags=["Building"])

BuildingServiceDep = Annotated[BuildingService, Depends(get_building_service)]


@router.get("/", response_model=list[BuildingRead])
async def get_all_buildings(service: BuildingServiceDep):
    return await service.get_all()


@router.get("/{build_id}", response_model=BuildingRead)
async def get_building_by_id(build_id: int, service: BuildingServiceDep):
    build = await service.get_by_id(build_id)
    if not build:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Building with this id does not exist"
        )
    return build


@router.post("/", response_model=BuildingRead)
async def create_building(build_in: BuildingCreate, service: BuildingServiceDep):
    try:
        return await service.create(build_in=build_in)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{build_id}", response_model=BuildingRead)
async def update_building(
    build_id: int,
    build_in: BuildingCreate,
    service: BuildingServiceDep,
):
    try:
        return await service.update(build_id=build_id, build_in=build_in)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{build_id}", response_model=None)
async def delete_building(build_id: int, service: BuildingServiceDep):
    try:
        return await service.delete(build_id=build_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
