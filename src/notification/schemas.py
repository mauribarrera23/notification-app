import pytz
import uuid

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, field_validator

from src.channel.schemas import ChannelSchema
from src.user.schemas import UserSchema


class NotificationSchema(BaseModel):
    id: uuid.UUID
    message: str
    created_at: datetime
    read: bool
    recipient_id: Optional[uuid.UUID]
    created_by: UserSchema
    channels: List[ChannelSchema]

    @field_validator(__field="created_at", mode="before")
    def convert_to_local_time(cls, value):
        timezone_local = pytz.timezone('America/Argentina/Catamarca')
        return value.replace(tzinfo=pytz.utc).astimezone(timezone_local)


class CreateNotification(BaseModel):
    message: str
    recipient_id: Optional[uuid.UUID] = None
    channel: Optional[ChannelSchema] = None
