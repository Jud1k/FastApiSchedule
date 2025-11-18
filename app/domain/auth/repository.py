import uuid

from sqlalchemy import select, update
from app.db.base_repository import SqlAlchemyRepository
from app.db.models import User


class UserRepository(SqlAlchemyRepository[User]):
    model = User

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        stmt = select(self.model).filter(self.model.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def update_user_password(self,user_id:uuid.UUID,new_password:str)->None:
        stmt = update(self.model).filter(self.model.id==user_id).values(password=new_password)
        await self.session.execute(stmt)
        return