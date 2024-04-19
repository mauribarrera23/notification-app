import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.channel.models import notification_channel
from src.settings.database import Base


class Notification(Base):
    __tablename__ = "notification"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    read = Column(Boolean, default=False, nullable=False)
    channels = relationship(
        'Channel',
        secondary=notification_channel,
        back_populates='notifications',
        cascade="all, delete",
        passive_deletes=True,
        lazy="selectin"
    )
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    recipient = relationship(
        "User",
        back_populates="notifications_received",
        foreign_keys=[recipient_id],
        lazy="selectin"
    )
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    created_by = relationship(
        "User",
        back_populates="notifications_sent",
        foreign_keys=[created_by_id],
        lazy="selectin"
    )
