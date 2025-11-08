import logging

from sqlalchemy.exc import IntegrityError

from app.building.repository import BuildingRepository
from app.building.schemas import BuildingCreate
from app.exceptions import ConflictError, NotFoundError
from app.shared.models import Building

logger = logging.getLogger(__name__)


class BuildingService:
    def __init__(self, session):
        self.build_repo = BuildingRepository(session)

    async def get_by_id(self, build_id: int) -> Building | None:
        build = await self.build_repo.get_one_or_none_by_id(id=build_id)
        return build

    async def get_all(self) -> list[Building]:
        build = await self.build_repo.get_all()
        return build

    async def create(self, build_in: BuildingCreate) -> Building:
        try:
            build_data = build_in.model_dump()
            building = await self.build_repo.create(data=build_data)
            return building
        except IntegrityError:
            raise ConflictError("Building with this name or address already exist")

    async def update(self, build_id: int, build_in: BuildingCreate) -> Building:
        build = await self.build_repo.get_one_or_none_by_id(id=build_id)
        if not build:
            logger.error(f"Building with {build_id} not found")
            raise NotFoundError(f"Building with {build_id} not found")
        try:
            build_data = build_in.model_dump()
            build = await self.build_repo.update(data=build, update_data=build_data)
            return build
        except IntegrityError as e:
            logger.error(e)
            raise ConflictError("Building with this name or addres already exist")

    async def delete(self, build_id: int):
        build = await self.build_repo.get_one_or_none_by_id(id=build_id)
        if not build:
            logger.error(f"Building with {build_id} not found")
            raise NotFoundError(f"Building with {build_id} not found")
        await self.build_repo.delete(id=build_id)
