from src.channel.constants import ErrorCode
from src.exceptions import BadRequest, NotFoundRequest


class ChannelNotFound(NotFoundRequest):
    DETAIL = ErrorCode.CHANNEL_NOT_FOUND


class ChannelSubscriptionExists(BadRequest):
    DETAIL = ErrorCode.CHANNEL_SUBSCRIPTION_EXISTS


class ChannelSubscriptionDoesntExists(BadRequest):
    DETAIL = ErrorCode.CHANNEL_SUBSCRIPTION_DOESNT_EXISTS


class ChannelRecipientSubscriptionDoesntExists(BadRequest):
    DETAIL = ErrorCode.CHANNEL_RECIPIENT_SUBSCRIPTION_DOESNT_EXISTS
