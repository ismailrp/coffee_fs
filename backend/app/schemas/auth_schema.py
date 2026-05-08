from pydantic import BaseModel
from pydantic import Field


class LoginSchema(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=3,
        max_length=100
    )