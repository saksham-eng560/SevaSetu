from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import datetime
from models.booking import Booking

class Provider(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    phone: str = Field(unique=True)
    category: str = Field(index=True)
    city: str
    experience_years: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default=None, datetime=datetime.datetime.utcnow())
    bookings: List["Booking"] = Relationship(back_populates="provider")