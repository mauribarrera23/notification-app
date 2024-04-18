import bcrypt
import jwt
import uuid

from datetime import datetime, timedelta
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.channel.models import user_channel
from src.settings.config import SECRET_KEY
from src.settings.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    channels = relationship('Channel', secondary=user_channel, back_populates='users', lazy="selectin")

    notifications_sent = relationship(
        "Notification",
        back_populates="created_by",
        foreign_keys="[Notification.created_by_id]",
        lazy="selectin"
    )
    notifications_received = relationship(
        "Notification",
        back_populates="recipient",
        foreign_keys="[Notification.recipient_id]",
        lazy="selectin"
    )

    @staticmethod
    def hash_password(password: str):
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        return password

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def generate_token(self):
        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration
        }
        return jwt.encode(payload, f"{SECRET_KEY}", algorithm="HS256")
