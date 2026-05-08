from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Coffee(Base):

    __tablename__ = "coffees"

    id = Column(Integer, primary_key=True, index=True)

    external_id = Column(Integer, unique=True)

    title = Column(String)

    description = Column(String)

    image = Column(String)
    orders = relationship(
        "Order",
        back_populates="coffee",
        cascade="all, delete"
    )