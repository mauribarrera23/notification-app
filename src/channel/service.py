import uuid
from typing import Any, Sequence

from sqlalchemy import insert, select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.channel.models import Channel, user_channel
from src.channel.schemas import CreateChannelSchema


async def create_channel(db: AsyncSession, data: CreateChannelSchema) -> dict[str, Any] | None:
    values = {"tag": data.tag}
    result = await db.execute(insert(Channel).values(**values).returning(Channel.id, Channel.tag))
    return result.fetchone()


async def get_channels(db: AsyncSession) -> Sequence[Channel]:
    result = await db.execute(select(Channel))
    channels = result.scalars().fetchall()
    return channels


async def get_channel_by_id(db: AsyncSession, channel_id: int) -> Channel | None:
    result = await db.execute(select(Channel).where(Channel.id == channel_id))
    channel = result.scalars().first()
    return channel


async def create_subscription(db: AsyncSession, channel_id: int, user_id: uuid.UUID) -> dict[str, Any] | None:
    subscription_values = {"channel_id": channel_id, "user_id": user_id}
    result = await db.execute(insert(user_channel).values(**subscription_values).returning(user_channel.c))
    return result.fetchone()


async def remove_subscription(db: AsyncSession, channel_id: int, user_id: uuid.UUID) -> None:
    await db.execute(delete(user_channel).where(and_(
        user_channel.c.channel_id == channel_id,
        user_channel.c.user_id == user_id,
    )))
