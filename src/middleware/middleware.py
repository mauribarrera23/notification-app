from fastapi import HTTPException, Request, status, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.user.utils import decode_jwt


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication credentials")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
            return credentials.credentials
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code")

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


class JWTBearerWebSocket(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, websocket: WebSocket):
        if not websocket.headers.get("Authorization"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Missing authentication token")
        auth_header = websocket.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        if not self.verify_jwt(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or token expired")
        return token

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
