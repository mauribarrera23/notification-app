
from pydantic import BaseModel


class CreateChannelSchema(BaseModel):
    tag: str


class ChannelSchema(CreateChannelSchema):
    id: int
