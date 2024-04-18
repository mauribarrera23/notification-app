import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse

from src.notification.exceptions import NotificationNotFound
from src.notification.service import (
    create_notification,
    delete_notification,
    get_notification_detail,
    get_received_notifications,
    get_sent_notifications,
    update_notification,
)
from src.settings.database import get_db_session
from src.user.dependencies import get_current_user
from src.notification.dependencies import notification_permission, validate_notification_creation
from src.notification.models import Notification
from src.notification.schemas import CreateNotification, NotificationSchema
from src.user.models import User

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=NotificationSchema)
async def create(
        data: CreateNotification = Depends(validate_notification_creation),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db_session)
):
    notification = await create_notification(db=db, data=data, user=user)
    return notification


@router.get("/received", status_code=status.HTTP_200_OK, response_model=List[NotificationSchema])
async def received_notification(db: AsyncSession = Depends(get_db_session), user: User = Depends(get_current_user)):
    notifications = await get_received_notifications(db=db, user=user)
    return notifications


@router.get("/sent", status_code=status.HTTP_200_OK, response_model=List[NotificationSchema])
async def sent_notification(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db_session)):
    notifications = await get_sent_notifications(db=db, user=user)
    return notifications


@router.get("/detail/{notification_id}", status_code=status.HTTP_200_OK, response_model=NotificationSchema)
async def detail_notification(
        notification_id: uuid.UUID,
        db: AsyncSession = Depends(get_db_session),
        user: User = Depends(get_current_user)
):
    notification = await get_notification_detail(db=db, notification_id=notification_id)
    if notification not in user.notifications_sent and notification not in user.notifications_received:
        raise NotificationNotFound()
    return notification


@router.put("/update/{notification_id}", status_code=status.HTTP_200_OK)
async def update_post(
        notification: Notification = Depends(notification_permission),
        db: AsyncSession = Depends(get_db_session)
):
    _notification = await update_notification(db=db, notification_id=notification.id, read=not notification.read)
    return {"message": "The notification has been updated successfully."}


@router.delete("/delete/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        notification: Notification = Depends(notification_permission),
        db: AsyncSession = Depends(get_db_session)
):
    await delete_notification(db=db, notification_id=notification.id)
    return {"message": "The notification has been deleted successfully."}
