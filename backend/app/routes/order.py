from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.order import Order
from app.models.coffee import Coffee

from app.auth.auth_bearer import verify_token
from app.logger import transaction_logger

from app.schemas.order_schema import OrderCreateSchema

router = APIRouter()


@router.post("/")
def create_order(
    payload: OrderCreateSchema,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    coffee = db.query(Coffee).filter(
        Coffee.id == payload.coffee_id
    ).first()

    if not coffee:

        raise HTTPException(
            status_code=404,
            detail="Coffee not found"
        )

    order = Order(
        user_id=1,
        coffee_id=payload.coffee_id,
        quantity=payload.quantity,
        notes=payload.notes
    )

    db.add(order)

    db.commit()
    transaction_logger.info(
    f"NEW ORDER | USER=1 "
    f"COFFEE={payload.coffee_id} "
    f"QTY={payload.quantity}"
)

    db.refresh(order)

    return order


@router.get("/")
def get_orders(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    return db.query(Order).all()