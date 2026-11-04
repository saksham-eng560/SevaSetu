# ServiceListResponse: status, count, items: list[ServiceItem] (same shape as ChaiMenu's MenuResponse
from pydantic import BaseModel
from typing import List

class ServiceListResponse(BaseModel):
    status: str
    count: int
    items: List[dict] 

class BulkList(BaseModel):
    found : int
    not_found : int
    serviceable : List[str]
    missing : List[str]

