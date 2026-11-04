from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime

class Review(SQLModel ,table = True):
    id : Optional[int] = Field(default=None, primary_key=True)
    booking_id : Optional[int] = Field(default=None, foreign_key="booking.id")
    provider_id : Optional[int] = Field(default=None, foreign_key="provider.id")
    rating : int = Field(ge=1, le=5)
    comment : str
    created_at : datetime = Field(default=None,datetime=datetime.datetime.utcnow())