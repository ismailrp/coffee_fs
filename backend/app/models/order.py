from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    coffee_id = Column(
        Integer,
        ForeignKey("coffees.id")
    )

    quantity = Column(Integer)

    notes = Column(String)

    coffee = relationship(
        "Coffee",
        back_populates="orders"
    )