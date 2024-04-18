import jwt
import time

from src.settings.config import SECRET_KEY


def decode_jwt(token: str) -> dict:
    decoded_token = jwt.decode(token, f"{SECRET_KEY}", algorithms=["HS256"])
    return decoded_token if decoded_token['exp'] >= time.time() else None
