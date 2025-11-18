import random
import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.building.schemas import BuildingCreate, BuildingUpdate
from app.domain.building.service import BuildingService
from app.exceptions import ConflictException, NotFoundException
from tests.factories import BuildingFactory


@pytest.mark.asyncio
async def test_get_buildings(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    created_buildings = await building_factory.create_batch_async(2)

    buildings = await service.get_all()
    assert len(buildings)==len(created_buildings)


@pytest.mark.asyncio
async def test_get_building(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    created_building = await building_factory.create_async()
    
    building = await service.get_by_id(created_building.id)
    assert building is not None
    assert building.id==created_building.id
    
    
@pytest.mark.asyncio
async def test_get_building_not_found(session:AsyncSession,building_factory:BuildingFactory):    
    service = BuildingService(session)
    building_id = random.randint(1,1_000_000)
    
    building = await service.get_by_id(building_id)
    assert building is None
    

@pytest.mark.asyncio
async def test_create_building(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    building_instance = building_factory.build()
    building_in = BuildingCreate.model_validate(building_instance)
    
    building = await service.create(building_in)
    assert building.name==building_in.name
    assert building.address==building_in.address
    
    with pytest.raises(ConflictException):
        await service.create(building_in)
    
@pytest.mark.asyncio
async def test_update_building(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    created_building = await building_factory.create_async()
    building_in = BuildingUpdate(name="New Name",address="New Address")
    
    building = await service.update(created_building.id,building_in)
    assert building.id==created_building.id
    assert building.name==building_in.name
    assert building.address==building_in.address
    
    
@pytest.mark.asyncio
async def test_update_building_not_found(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    building_instance = building_factory.build()
    building_in = BuildingUpdate(name="New Name",address="New Address")
    
    with pytest.raises(NotFoundException):
        await service.update(building_instance.id,building_in)
        
        
@pytest.mark.asyncio
async def test_update_bulding_conflict(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    created_buildings = await building_factory.create_batch_async(2)
    building_in = BuildingUpdate.model_validate(created_buildings[0],from_attributes=True)
    
    with pytest.raises(ConflictException):
        await service.update(created_buildings[1].id,building_in)
    
    
@pytest.mark.asyncio
async def test_delete_building(session:AsyncSession,building_factory:BuildingFactory):
    service = BuildingService(session)
    created_building = await building_factory.create_async()
    
    building = await service.delete(created_building.id)
    assert building is None
    
    with pytest.raises(NotFoundException):
        await service.delete(created_building.id)