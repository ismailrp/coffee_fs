import requests

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.coffee import Coffee
from app.auth.auth_bearer import verify_token

from app.schemas.coffee_schema import (
    CoffeeCreateSchema,
    CoffeeUpdateSchema
)

router = APIRouter()


@router.post("/import")
def import_coffees(db: Session = Depends(get_db)):

    url = "https://api.sampleapis.com/coffee/iced"

    try:

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"External API error: {str(e)}"
        )

    if not isinstance(data, list):

        raise HTTPException(
            status_code=500,
            detail="Invalid API response"
        )

    inserted = 0

    for item in data:

        external_id = item.get("id")

        if not external_id:
            continue

        exists = db.query(Coffee).filter(
            Coffee.external_id == external_id
        ).first()

        if exists:
            continue

        coffee = Coffee(
            external_id=external_id,
            title=item.get("title"),
            description=item.get("description"),
            image=item.get("image")
        )

        db.add(coffee)

        inserted += 1

    db.commit()

    return {
        "success": True,
        "inserted": inserted
    }


@router.get("/")
def get_coffees(
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    coffees = db.query(Coffee).all()

    return coffees

@router.post("/")
def create_coffee(
    payload: CoffeeCreateSchema,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    coffee = Coffee(
        title=payload.title,
        description=payload.description,
        image=payload.image
    )

    db.add(coffee)

    db.commit()

    db.refresh(coffee)

    return coffee

@router.put("/{coffee_id}")
def update_coffee(
    coffee_id: int,
    payload: CoffeeUpdateSchema,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    coffee = db.query(Coffee).filter(
        Coffee.id == coffee_id
    ).first()


    if not coffee:

        raise HTTPException(
            status_code=404,
            detail="Coffee not found"
        )

    if payload.title is not None:
        coffee.title = payload.title

    if payload.description is not None:
        coffee.description = payload.description

    if payload.image is not None:
        coffee.image = payload.image


    db.commit()

    return coffee

@router.delete("/{coffee_id}")
def delete_coffee(
    coffee_id: int,
    user=Depends(verify_token),
    db: Session = Depends(get_db)
):

    coffee = db.query(Coffee).filter(
        Coffee.id == coffee_id
    ).first()

    if not coffee:

        raise HTTPException(
            status_code=404,
            detail="Coffee not found"
        )

    db.delete(coffee)

    db.commit()

    return {
        "message": "Coffee deleted"
    }