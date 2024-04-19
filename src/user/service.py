import uuid
from typing import List

from sqlalchemy import insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User
from src.user.schemas import UserCreate


async def create_user(db: AsyncSession, data: UserCreate) -> None:
    hashed_password = User.hash_password(data.password)
    user_values = {"username": data.username, "email": data.email, "password": hashed_password}
    await db.execute(insert(User).values(**user_values))
    await db.commit()


async def get_user_valid_creation(db: AsyncSession, username: str, email: str) -> User | None:
    user = (await db.scalars(select(User).where(or_(User.username == username, User.email == email)))).first()
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    user = (await db.scalars(select(User).where(User.username == username))).first()
    return user


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    user = (await db.scalars(select(User).where(User.id == user_id))).first()
    return user


async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    users = [row[0] for row in result.fetchall()]
    return users
