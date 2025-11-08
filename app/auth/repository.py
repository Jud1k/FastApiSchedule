from app.shared.base_repository import SqlAlchemyRepository
from app.shared.models import User


class UserRepository(SqlAlchemyRepository[User]):
    model = User
