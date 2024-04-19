from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.channel.dependencies import validate_subscription, validate_unsubscript
from src.channel.models import Channel
from src.channel.schemas import ChannelSchema, CreateChannelSchema
from src.channel.service import create_channel, create_subscription, get_channels, remove_subscription
from src.settings.database import get_db_session
from src.user.dependencies import get_current_user
from src.user.models import User

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ChannelSchema)
async def new_channel(
        data: CreateChannelSchema,
        _: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    channel = await create_channel(db=db, data=data)
    return channel


@router.get("/list", status_code=status.HTTP_200_OK, response_model=List[ChannelSchema])
async def list_channels(_: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    channels = await get_channels(db=db)
    return channels


@router.put("/subscribe/{channel_id}", status_code=status.HTTP_200_OK)
async def subscribe_channel(
        channel_id: int = Depends(validate_subscription),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    await create_subscription(db=db, channel_id=channel_id, user_id=user.id)
    return {"message": f"The user has subscribed to the channel"}


@router.delete("/unsubscribe/{channel_id}", status_code=status.HTTP_200_OK)
async def unsubscribe_channel(
        channel_id: int = Depends(validate_unsubscript),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    await remove_subscription(db=db, channel_id=channel_id, user_id=user.id)
    return {"message": f"The user has unsubscribed to the channel"}
