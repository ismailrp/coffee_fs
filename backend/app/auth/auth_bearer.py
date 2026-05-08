from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from fastapi import HTTPException
from fastapi import Depends

from jose import jwt
from jose.exceptions import JWTError

SECRET_KEY = "SUPERSECRETKEY"

ALGORITHM = "HS256"

security = HTTPBearer()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )