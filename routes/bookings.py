from fastapi import APIRouter, HTTPException, Depends
from app.database import get_session
from typing import Optional,List
from sqlmodel import select
from models.booking import Booking


bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])

@bookings_router.get("/}")
def get_bookings_list(bookingList : List[Booking],Session = Depends(get_session)):
    """
    Get a list of bookings.
    """
    finallist = []
    for booking in bookingList:
        response = Session.exec(select(Booking).where(Booking.id == booking.id)).first()
        finallist.append(response.model_dump())
    return {"bookings": finallist}

@bookings_router.post("/")
def create_booking(booking: Booking, Session = Depends(get_session)):
    """
    Create a new booking.
    """
    new_booking = Booking.model_validate(booking)
    new_booking.total_amount = booking.quantity * 100.0  # Assuming a fixed price of 100 per unit
    Session.add(new_booking)
    Session.commit()
    Session.refresh(new_booking)
    return {"booking": new_booking.model_dump()}

@bookings_router.get("/{booking_id}", response_model=Booking)
def get_booking_by_id(booking_id: int, Session = Depends(get_session)):
    """
    Get details of a specific booking by its ID.
    """
    booking = Session.exec(select(Booking).where(Booking.id == booking_id)).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return booking.model_dump()