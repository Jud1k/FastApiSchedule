from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import Building


class BuildingRepository(SqlAlchemyRepository[Building]):
    model = Building
