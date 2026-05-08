from pydantic import BaseModel
from pydantic import Field


class CoffeeCreateSchema(BaseModel):

    title: str = Field(
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    image: str | None = None


class CoffeeUpdateSchema(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=500
    )

    image: str | None = None