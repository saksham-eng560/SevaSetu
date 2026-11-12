from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime

# ---------------------------------------------------------------------------
# NOTE: no top-level `from models.customer import Customer` anymore.
# That was the circular import: booking.py -> customer.py -> booking.py.
# The imports now live at the BOTTOM of this file (see end of file).
# ---------------------------------------------------------------------------


class Booking(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    customer_id : Optional[int] = Field(default=None, foreign_key="customer.id")
    pincode : str
    address : str
    # BUG FIX: `datetime` alone is the *module*. The type is datetime.datetime.
    scheduled_for : datetime.datetime
    quantity : int = Field(ge=1, le=5)
    total_amount : float
    status : str = Field(default="pending")
    # BUG FIX: `datetime=...` is not a Field argument, and calling utcnow()
    # would freeze the time at import. default_factory takes the function
    # itself and calls it for each new row.
    created_at : datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    # Quoted names are forward references (plain strings). At this point in
    # the file `Customer` / `Review` don't exist yet, so they stay unresolved
    # until the bottom imports + model_rebuild() below.
    customer: Optional["Customer"] = Relationship(back_populates="bookings")
    review : Optional["Review"] = Relationship(back_populates="booking")


# ---------------------------------------------------------------------------
# BOTTOM IMPORT + model_rebuild()  (the approach used)
# ---------------------------------------------------------------------------
# Why it works: by the time Python reaches these lines, `Booking` already
# exists in this module. So if customer.py runs `from models.booking import
# Booking` while we're still importing it, that succeeds (the module is
# half-loaded in sys.modules, but the name is defined).
#
# model_rebuild() (Pydantic v2) re-resolves the string annotations
# "Customer" / "Review" now that those classes are importable.
#
# Caveat: these imports MUST stay below the class. Move them to the top
# and the cycle comes back. Linters complain, hence the noqa.
from models.customer import Customer  # noqa: E402,F401
from models.review import Review      # noqa: E402,F401

Booking.model_rebuild()


# ---------------------------------------------------------------------------
# Alternative (for study, NOT used): TYPE_CHECKING
# ---------------------------------------------------------------------------
#   from typing import TYPE_CHECKING
#   if TYPE_CHECKING:
#       from models.customer import Customer
#       from models.review import Review
#
# TYPE_CHECKING is False at runtime, so the imports never execute and the
# cycle can't happen; editors still see the types. Relationship targets are
# then resolved by SQLAlchemy by class name, so every model module just has
# to be imported somewhere before the first query.
