from typing import Annotated

import jwt

from fastapi import Depends
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.middleware.middleware import JWTBearer, JWTBearerWebSocket
from src.settings.database import get_db_session
from src.user.exceptions import EmailExists, InvalidCredentials, InvalidToken, UsernameExists
from src.settings.config import SECRET_KEY
from src.user.schemas import UserCreate
from src.user.service import get_user_by_id, get_user_valid_creation


async def validate_user_creation(data: UserCreate, db: AsyncSession = Depends(get_db_session)):
    user = await get_user_valid_creation(db, data.username, data.email)
    if not user:
        return data
    if user.username == data.username:
        raise UsernameExists()
    if user.email == data.email:
        raise EmailExists()


async def get_current_user(db: AsyncSession = Depends(get_db_session), token: str = Depends(JWTBearer())):
    try:
        payload = jwt.decode(token, f"{SECRET_KEY}", algorithms=["HS256"])
        user_id = payload.get("sub")
        user = await get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise InvalidCredentials()
        return user
    except (PyJWTError, AttributeError):
        return InvalidToken()


async def get_websocket_current_user(db: AsyncSession = Depends(get_db_session), token: str = Depends(JWTBearerWebSocket())):
    try:
        payload = jwt.decode(token, f"{SECRET_KEY}", algorithms=["HS256"])
        user_id = payload.get("sub")
        user = await get_user_by_id(db=db, user_id=user_id)
        if not user:
            raise InvalidCredentials()
        return user
    except (PyJWTError, AttributeError):
        return InvalidToken()
