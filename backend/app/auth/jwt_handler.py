from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SUPERSECRETKEY"

ALGORITHM = "HS256"


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = datetime.utcnow() + timedelta(hours=2)

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )