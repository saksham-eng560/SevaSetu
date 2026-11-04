from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from routes.services import router
from routes.areas import arearouter
from app.exceptions import InvalidPincodeError, PincodeNotServiceableError, ServiceUnavailableError
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")

app = FastAPI(
    title="SevaSetu",
    description="SevaSetu is a platform for providing services to the people",
    version="1.0.0",
    lifespan = lifespan
)

app.include_router(router)
app.include_router(arearouter)

@app.get("/",tags=["Root"])
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health",tags=["Root"])
def health_check():
    return {"status": "healthy"}