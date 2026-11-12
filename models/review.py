from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime


class Review(SQLModel ,table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    booking_id : Optional[int] = Field(default=None, foreign_key="booking.id")
    rating : int = Field(ge=1, le=5)
    comment : str
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    # Booking.review uses back_populates="booking", so this side must exist
    # with that exact name, otherwise SQLAlchemy raises at mapper setup.
    booking : Optional["Booking"] = Relationship(back_populates="review")


# Bottom import + model_rebuild(): same pattern as booking.py / customer.py.
from models.booking import Booking  # noqa: E402,F401

Review.model_rebuild()
