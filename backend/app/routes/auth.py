from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.user import User

from app.auth.password_handler import verify_password
from app.auth.jwt_handler import create_access_token

from app.schemas.auth_schema import LoginSchema

router = APIRouter()


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.username == payload.username
    ).first()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username"
        )

    valid = verify_password(
        payload.password,
        user.password
    )

    if not valid:

        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "sub": user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }