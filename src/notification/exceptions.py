from src.notification.constants import ErrorCode
from src.exceptions import NotFoundRequest, UnauthorizedRequest


class NotificationNotFound(NotFoundRequest):
    DETAIL = ErrorCode.NOTIFICATION_NOT_FOUND


class NotificationPermission(UnauthorizedRequest):
    DETAIL = ErrorCode.NOTIFICATION_UNAUTHORIZED
