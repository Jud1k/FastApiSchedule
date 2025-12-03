import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import engine
from app.db.models import User
from app.core.config import settings
from app.domain.auth.repository import UserRepository
from app.domain.auth.schemas import UserCreate


async def init():
    async with AsyncSession(engine) as session:  
        result = await session.execute(select(User).where(User.email==settings.FIRST_SUPERUSER))
        user = result.scalar_one_or_none()
        if not user:
            user_in = UserCreate(email=settings.FIRST_SUPERUSER,password=settings.FIRST_SUPERUSER_PASSWORD,role="admin")
            repo = UserRepository(session)
            await repo.create(user_in) 
            await session.commit()

async def main():
    print("Creating initial data")
    await init()
    print("Initial data created")
    
if __name__=="__main__":
    asyncio.run(main())