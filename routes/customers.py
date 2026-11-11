from fastapi import APIRouter, Depends
from app.database import get_session
from typing import List
from sqlmodel import select, Session
from models.customer import Customer

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
