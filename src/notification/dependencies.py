import uuid

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.channel.dependencies import validate_channel
from src.channel.exceptions import ChannelRecipientSubscriptionDoesntExists, ChannelSubscriptionDoesntExists
from src.notification.exceptions import NotificationNotFound, NotificationPermission
from src.notification.models import Notification
from src.notification.schemas import CreateNotification
from src.notification.service import get_notification_detail
from src.settings.database import get_db_session
from src.user.dependencies import get_current_user
from src.user.models import User
from src.user.service import get_user_by_id


async def notification_permission(
        notification_id: uuid.UUID,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
) -> Notification | HTTPException:
    notification = await get_notification_detail(db=db, notification_id=notification_id)
    if not notification:
        raise NotificationNotFound()
    if notification not in current_user.notifications_sent:
        raise NotificationPermission()
    return notification


async def validate_notification_creation(
        data: CreateNotification,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
) -> CreateNotification | HTTPException:
    channel = await validate_channel(db=db, channel_id=data.channel.id)
    recipient = await get_user_by_id(db=db, user_id=data.recipient_id)
    if channel not in current_user.channels:
        raise ChannelSubscriptionDoesntExists()
    if data.recipient_id and channel not in recipient.channels:
        raise ChannelRecipientSubscriptionDoesntExists()
    return data

