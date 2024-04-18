import uuid

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: uuid.UUID
    email: str
    username: str


class UserCreate(BaseModel):
    email: str
    password: str
    username: str


class UserLogin(BaseModel):
    password: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
