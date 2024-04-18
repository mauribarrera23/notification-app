from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.channel.models import Channel
from src.channel.service import get_channel_by_id
from src.channel.exceptions import ChannelNotFound, ChannelSubscriptionDoesntExists, ChannelSubscriptionExists
from src.settings.database import get_db_session

from src.user.dependencies import get_current_user
from src.user.models import User


async def validate_channel(channel_id: int, db: AsyncSession) -> Channel | HTTPException:
    channel = await get_channel_by_id(db=db, channel_id=channel_id)
    if not channel:
        raise ChannelNotFound()
    return channel


async def validate_subscription(
        channel_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
) -> Channel | HTTPException:
    channel = await validate_channel(db=db, channel_id=channel_id)
    if channel in current_user.channels:
        raise ChannelSubscriptionExists()
    return channel


async def validate_unsubscript(
        channel_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
) -> Channel | HTTPException:
    channel = await validate_channel(db=db, channel_id=channel_id)
    if channel not in current_user.channels:
        raise ChannelSubscriptionDoesntExists()
    return channel
