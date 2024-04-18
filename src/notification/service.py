import uuid
from typing import List

from sqlalchemy import and_, insert, or_, select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.channel.models import notification_channel, Channel
from src.channel.service import get_channel_by_id
from src.notification.models import Notification
from src.notification.schemas import CreateNotification
from src.user.models import User


async def create_notification(db: AsyncSession, data: CreateNotification, user: User) -> Notification | None:
    values = {
        "created_by_id": user.id,
        "message": data.message,
        "recipient_id": data.recipient_id,
    }

    result = await db.execute(insert(Notification).values(**values).returning(Notification))
    notification = result.fetchone()
    if not notification:
        return None
    channel = await get_channel_by_id(db=db, channel_id=data.channel.id)
    notification[0].channels.append(channel)
    return notification[0]


async def get_notification_detail(db: AsyncSession, notification_id: uuid.UUID) -> Notification | None:
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    notification = result.scalars().first()
    return notification


async def get_received_notifications(db: AsyncSession, user: User) -> List[Notification]:
    subscribed_channel_ids = [channel.id for channel in user.channels]
    query = select(Notification).join(notification_channel).join(Channel).where(
        and_(
            notification_channel.c.notification_id == Notification.id,
            notification_channel.c.channel_id == Channel.id,
            Channel.id.in_(subscribed_channel_ids),
            or_(
                Notification.recipient_id == user.id,
                Notification.recipient_id == None   # noqa
            )
        )
    )
    result = await db.execute(query)
    notifications = [row[0] for row in result.fetchall()]
    return notifications


async def get_sent_notifications(db: AsyncSession, user: User) -> List[Notification]:
    result = await db.execute(select(Notification).where(Notification.created_by_id == user.id)) # noqa
    notifications = [row[0] for row in result.fetchall()]
    return notifications


async def update_notification(db: AsyncSession, notification_id: uuid.UUID, read: bool) -> Notification | None:
    notification_values = {"read": read}
    result = await db.execute(
        update(Notification)
        .where(Notification.id == notification_id)
        .values(**notification_values)
        .returning(Notification)
    )
    notification = result.fetchone()
    return notification


async def delete_notification(db: AsyncSession, notification_id: uuid.UUID) -> None:
    await db.execute(delete(Notification).where(Notification.id == notification_id))
