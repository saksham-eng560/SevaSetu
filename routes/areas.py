from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Optional, List
from app.exceptions import InvalidPincodeError, PincodeNotServiceableError, ServiceUnavailableError
from app.data import servicable_pincodes,services_we_provide
from pydantic import BaseModel
from models.response import BulkList
# exception handlers
def handle_invalid_pincode_error(request, exc: InvalidPincodeError):
    return JSONResponse(
        status_code=400,
        content={"message": f"Invalid pincode: {exc.pincode}. Pincode must be 6 digits."},
    )
def handle_pincode_not_serviceable_error(request, exc: PincodeNotServiceableError):
    return JSONResponse(
        status_code=404,
        content={"message": f"Pincode {exc.pincode} is not serviceable."},
    )
def handle_service_unavailable_error(request, exc: ServiceUnavailableError):
    return JSONResponse(
        status_code=409,
        content={"message": f"Service with ID {exc.service_id} is currently unavailable."},
    )

class bulkList(BaseModel):
    pincode : List[str]

arearouter = APIRouter(prefix="/areas",tags=["Areas"])

@arearouter.get("/cities")
def get_cities():
    """
    Get a list of cities we service.
    """
    if not services_we_provide:
        raise ServiceUnavailableError(service_id=1)  # Example service_id
    finalist = []
    for city in services_we_provide:
        if city not in finalist:
            finalist.append(city)
    if len(finalist) == 0:
        raise ServiceUnavailableError(service_id=1)  # Example service_id
    return {"cities": finalist}

@arearouter.get("/{pincode}")
def get_area_by_pincode(pincode: str):
    """
    Get details of a specific area by its pincode.
    """
    from app.data import servicable_pincodes  
    if len(pincode) != 6 or not pincode.isdigit():
        raise InvalidPincodeError(pincode)
    if pincode in servicable_pincodes:
        return servicable_pincodes[pincode]
    raise PincodeNotServiceableError(pincode)

@arearouter.post("/check-bulk",response_model=BulkList)
def bulker(pincodeList : Optional[bulkList] = None):
    """
    Check a list of pincodes for serviceability.
    """    
    found = 0
    not_found = 0
    serviceable = []
    missing = []
    
    for pincode in pincodeList.pincode:
        if len(pincode) != 6 or not pincode.isdigit():
            missing.append(pincode)
            not_found += 1
            continue
        if pincode in servicable_pincodes:
            found += 1
            serviceable.append(pincode)
        else:
            not_found += 1
            missing.append(pincode)
    
    return BulkList(
        found=found,
        not_found=not_found,
        serviceable=serviceable,
        missing=missing
    )

