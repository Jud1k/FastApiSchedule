import random
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.custom_redis import CustomRedis
from app.domain.group.schemas import GroupCreate, GroupUpdate
from app.domain.group.service import GroupService
from app.exceptions import ConflictException, NotFoundException
from tests.factories import GroupFactory


@pytest.mark.asyncio()
async def test_get_groups(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    created_groups = await group_factory.create_batch_async(2)
    
    groups = await service.get_all()
    assert len(groups) == len(created_groups)
    
    
@pytest.mark.asyncio()
async def test_get_group(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    created_group = await group_factory.create_async()
    
    group=await service.get_by_id(created_group.id)
    assert group is not None
    assert group.id==created_group.id
    assert group.name==created_group.name
    assert group.course==created_group.course
    assert group.institute==created_group.institute
    

@pytest.mark.asyncio
async def test_get_groups_summary(session: AsyncSession, redis: CustomRedis, group_factory: GroupFactory):
    service = GroupService(session,redis)
    created_groups = await group_factory.create_batch_async(2)
    
    groups = await service.get_groups_summary()
    assert len(groups) == len(created_groups)
        
@pytest.mark.asyncio()
async def test_get_group_not_found(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    group_id = random.randint(1,1_000_000)
    
    group=await service.get_by_id(group_id)
    assert group is None
    

@pytest.mark.asyncio()
async def test_create_group(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    group_in = GroupCreate(name="TestGroup",course=1,institute="TestInstitute")
    
    group = await service.create(group_in)
    assert group.name==group_in.name
    assert group.course==group_in.course
    assert group.institute==group_in.institute
    
    with pytest.raises(ConflictException):
        await service.create(group_in)
        

@pytest.mark.asyncio()
async def test_update_group(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    created_group = await group_factory.create_async()
    group_in = GroupUpdate(name="NewGroup",course=1,institute="NewInstitute")
    
    group = await service.update(created_group.id,group_in)
    assert group.name==group_in.name
    assert group.course==group_in.course
    assert group.institute==group_in.institute
    
    
@pytest.mark.asyncio
async def test_update_group_not_found(session: AsyncSession, redis: CustomRedis, group_factory: GroupFactory):
    service = GroupService(session, redis)
    group_id = random.randint(1, 1_000_000)
    group_in = GroupUpdate(name="NewGroup", course=1, institute="NewInstitute")
    
    with pytest.raises(NotFoundException):
        await service.update(group_id, group_in)
    
    
@pytest.mark.asyncio
async def test_update_group_conflic(session: AsyncSession, redis: CustomRedis, group_factory: GroupFactory):
    service = GroupService(session, redis)
    created_group = await group_factory.create_batch_async(2)
    group_in = GroupUpdate(name=created_group[0].name, course=1, institute="NewInstitute")
    
    with pytest.raises(ConflictException):
        await service.update(created_group[1].id, group_in)
        
        
@pytest.mark.asyncio()
async def test_delete_group(session:AsyncSession,redis:CustomRedis,group_factory:GroupFactory):
    service = GroupService(session,redis)
    created_group = await group_factory.create_async()
    
    group = await service.delete(created_group.id)
    assert group is None
    
    
@pytest.mark.asyncio
async def test_delete_group_not_found(session: AsyncSession, redis: CustomRedis, group_factory: GroupFactory):
    service = GroupService(session, redis)
    group_id = random.randint(1, 1_000_000)
    with pytest.raises(NotFoundException):
        await service.delete(group_id)