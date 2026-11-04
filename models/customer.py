from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from models.booking import Booking
from typing import List
from pydantic import field_validator


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone_number: str
    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value : str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be a 10-digit number.")
        return value
    pincode: str
    address: str
    pincode: str
    created_at: datetime = Field(default=None,datetime=datetime.datetime.utcnow())
    bookings : List[Booking] = Relationship(back_populates="customer")