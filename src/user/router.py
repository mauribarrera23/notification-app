from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings.database import get_db_session
from src.user import service
from src.user.dependencies import get_current_user, validate_user_creation
from src.user.exceptions import InvalidCredentials
from src.user.schemas import Token, UserCreate, UserLogin, UserSchema
from src.user.service import get_user_by_username

router = APIRouter()


@router.post(path="/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: UserCreate = Depends(validate_user_creation), db: AsyncSession = Depends(get_db_session)):
    await service.create_user(db, data)
    return {"message": "User has been created"}


@router.post(path="/login", status_code=status.HTTP_200_OK)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_username(db=db, username=data.username)
    if user is None or not user.verify_password(password=data.password):
        raise InvalidCredentials()
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(user=Depends(get_current_user), _: AsyncSession = Depends(get_db_session)):
    return user
