from pydantic import BaseModel
from pydantic import Field


class OrderCreateSchema(BaseModel):

    coffee_id: int

    quantity: int = Field(
        gt=0,
        le=100
    )

    notes: str | None = Field(
        default=None,
        max_length=300
    )