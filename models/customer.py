from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from models.booking import Booking
from typing import List

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone_number: str
    pincode: str
    address: str
    pincode: str
    created_at: datetime = Field(default=None,datetime=datetime.datetime.utcnow())
    bookings : List[Booking] = Relationship(back_populates="customer")