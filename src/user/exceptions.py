from src.user.constants import ErrorCode
from src.exceptions import BadRequest, ForbiddenRequest


class UsernameExists(BadRequest):
    DETAIL = ErrorCode.USER_USERNAME_EXISTS


class EmailExists(BadRequest):
    DETAIL = ErrorCode.USER_EMAIL_EXISTS


class InvalidCredentials(BadRequest):
    DETAIL = ErrorCode.USER_INVALID_CREDENTIALS


class InvalidToken(ForbiddenRequest):
    DETAIL = ErrorCode.USER_INVALID_TOKEN
