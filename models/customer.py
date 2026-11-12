from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import datetime
from pydantic import field_validator

# NOTE: `from models.booking import Booking` used to be here (top). It's now
# at the bottom of the file to break the circular import.


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
    # (removed duplicate `pincode: str` declaration)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    # BUG FIX: was `List[Booking]` (unquoted), which needs the real class at
    # class-creation time. Quoting makes it a forward reference.
    bookings : List["Booking"] = Relationship(back_populates="customer")


# ---------------------------------------------------------------------------
# BOTTOM IMPORT + model_rebuild()  (the approach used)
# ---------------------------------------------------------------------------
# `Customer` is already defined here, so when booking.py does
# `from models.customer import Customer` mid-import, it succeeds.
# model_rebuild() then resolves the "Booking" forward reference.
from models.booking import Booking  # noqa: E402,F401

Customer.model_rebuild()


# Alternative (not used): `if TYPE_CHECKING:` import at the top.
# See the note at the bottom of models/booking.py.
