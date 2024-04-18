from sqlalchemy import Column, ForeignKey, Integer, String, Table, UUID
from sqlalchemy.orm import relationship

from src.settings.database import Base

user_channel = Table(
    'user_channel', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), primary_key=True),
)

notification_channel = Table(
    'notification_channel', Base.metadata,
    Column('notification_id', UUID(as_uuid=True), ForeignKey('notification.id'), primary_key=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), primary_key=True),
)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, nullable=False)
    users = relationship('User', secondary=user_channel, back_populates='channels')
    notifications = relationship(
        'Notification',
        secondary=notification_channel,
        back_populates='channels'
    )
