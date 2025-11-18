import logging

from sqlalchemy.exc import IntegrityError

from app.domain.building.repository import BuildingRepository
from app.domain.building.schemas import BuildingCreate,BuildingUpdate
from app.exceptions import ConflictException, NotFoundException
from app.db.models import Building

logger = logging.getLogger(__name__)


class BuildingService:
    def __init__(self, session):
        self.building_repo = BuildingRepository(session)

    async def get_by_id(self, building_id: int) -> Building | None:
        build = await self.building_repo.get_one_or_none_by_id(id=building_id)
        return build

    async def get_all(self) -> list[Building]:
        build = await self.building_repo.get_all()
        return build

    async def create(self, building_in: BuildingCreate) -> Building:
        try:
            building = await self.building_repo.create(data=building_in)
            return building
        except IntegrityError as e:
            logger.error(f"Integirity error while created Building:{str(e)}")
            raise ConflictException("Building")
        
    async def update(self, building_id: int, building_in: BuildingUpdate) -> Building:
        building = await self.building_repo.get_one_or_none_by_id(id=building_id)
        if not building:
            raise NotFoundException("Building", building_id)
        try:
            building = await self.building_repo.update(data=building, update_data=building_in)
            return building
        except IntegrityError as e:
            logger.error(f"Integirity error while updating Building:{str(e)}")
            raise ConflictException("Building")

    async def delete(self, building_id: int)->None:
        building = await self.building_repo.get_one_or_none_by_id(id=building_id)
        if not building:
            raise NotFoundException("Building",building_id)
        await self.building_repo.delete(id=building_id)
