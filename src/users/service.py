from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from users.model import User
from users.schemas import UserCreate



async def get_user(user_id: int, session: AsyncSession):
    return await session.get(User, user_id)


async def get_users(session: AsyncSession):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)



async def create_users(user: UserCreate, session: AsyncSession):
    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    return user