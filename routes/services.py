from app.data import services_we_provide
from fastapi import APIRouter, HTTPException
from typing import Optional
from models.response import ServiceListResponse

router = APIRouter(prefix="/services",tags=["Services"])

@router.get("/",response_model=ServiceListResponse)
def get_services(category: Optional[str] = None,active: Optional[bool] = None):
    """
    Get a list of services we provide.
    Optional query parameters:
    - category: filter by service category (e.g., "plumbing", "electrical")
    - active: filter by active status (True or False)
    """
    filtered_services = [s for s in services_we_provide if s["active"] == active]  # Start with active services only
    final_services = []
    for service in filtered_services:
        if service["category"] == category and service["active"] == active:
            final_services.append(service)
    if len(final_services) == 0:
        raise HTTPException(status_code=404, detail="No services found for the given category and active status.")
    return ServiceListResponse(
        status="active",
        count=len(final_services),
        items=final_services
    )

@router.get("/{service_id}")
def get_service_by_id(service_id: int):
    """
    Get details of a specific service by its ID.
    """
    for service in services_we_provide:
        if service["id"] == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found.")

    
