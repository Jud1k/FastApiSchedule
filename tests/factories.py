from faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from factory import Sequence
from factory.fuzzy import FuzzyText
from sqlalchemy.orm import Session

from app.db.models import Room

faker = Faker()


class BaseFactory(SQLAlchemyModelFactory):
    """Base Factory"""

    class Meta:
        sqlalchemy_session = Session()


class RoomFactory(BaseFactory):
    id = Sequence(lambda n: n)
    name = FuzzyText()

    class Meta:
        model = Room