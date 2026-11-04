from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime
from models.customer import Customer
from models.review import Review

class Booking(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    customer_id : Optional[int] = Field(default=None, foreign_key="customer.id")
    service_id : Optional[int] = Field(default=None, foreign_key="service.id")
    pincode : str
    address : str
    scheduled_for : datetime
    quantity : int = Field(ge=1, le=5)
    total_amount : float
    status : str = Field(default="pending")
    created_at : datetime = Field(default=None,datetime=datetime.datetime.utcnow())
    customer: Optional["Customer"] = Relationship(back_populates="bookings")
    review : Optional["Review"] = Relationship(back_populates="booking")
