from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from typing import List
from sqlmodel import select, Session
from models.customer import Customer
from models.booking import Booking

router_customer = APIRouter(prefix="/customers", tags=["Customers"])

@router_customer.get("/retrieve")
def get_customers_list(Session: Session = Depends(get_session)):
    """
    Get a list of customers.
    """
    customers = Session.exec(select(Customer)).all()
    return {"customers": [customer.model_dump() for customer in customers]}

@router_customer.post("/create")
def create_customer(customer: Customer, Session: Session = Depends(get_session)):
    """
    Create a new customer.
    """
    customers = Session.exec(select(Customer)).first()
    if customers and customers.email == customer.email:
        raise HTTPException(status_code=400, detail="Customer with this email already exists.")
    if customers and customers.phone_number == customer.phone_number:
        raise HTTPException(status_code=422, detail="Customer with this phone number already exists.")
    new_customer = Customer.model_validate(customer)

    Session.add(new_customer)
    Session.commit()
    Session.refresh(new_customer)
    return {"customer": new_customer.model_dump()}

@router_customer.patch("/update/{customer_id}")
def update_customer(customer_id: int, customer: Customer, Session: Session = Depends(get_session
)):
    """
    Update an existing customer.
    """
    existing_customer = Session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if not existing_customer:
        return {"error": "Customer not found."}
    
    existing_customer_dict = existing_customer.model_dump()
    for key, value in existing_customer_dict.items():
        if hasattr(customer, key) and getattr(customer, key) is not None:
            existing_customer_dict[key] = getattr(customer, key)
            

    Session.add(existing_customer)
    Session.commit()
    Session.refresh(existing_customer)
    return {"customer": existing_customer.model_dump()}

@router_customer.delete("/delete/{customer_id}")
def delete_customer(customer_id: int, Session: Session = Depends(get_session)):
    """
    Delete a customer by ID.
    """
    existing_customer = Session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if not existing_customer:
        return {"error": "Customer not found."}
    
    Session.delete(existing_customer)
    Session.commit()
    return {"message": "Customer deleted successfully."}

@router_customer.get("/{id}/bookings")
def get_customer_bookings(id: int, Session: Session = Depends(get_session)):
    """
    Get a list of bookings for a specific customer by their ID.
    """
    response = Session.exec(select(Booking).where(Booking.booking_id == id)).all()
    customer = []
    for r in response:
        customer.append(r)

    if len(customer) == 0:
        raise HTTPException(status_code=404, detail="Customer not found.")
   
    return {"bookings": customer}