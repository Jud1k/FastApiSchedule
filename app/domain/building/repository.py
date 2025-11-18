from app.db.base_repository import SqlAlchemyRepository
from app.db.models import Building


class BuildingRepository(SqlAlchemyRepository[Building]):
    model = Building
