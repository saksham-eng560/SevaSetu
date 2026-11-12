from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from routes.services import router
from routes.areas import arearouter
from routes.bookings import bookings_router
from routes.customers import router_customer
from routes.reviews import router_review
from app.exceptions import InvalidPincodeError, PincodeNotServiceableError, ServiceUnavailableError
from app.database import create_table, get_session

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_table()
    print("Database tables created.")
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
app.include_router(bookings_router)
app.include_router(router_customer)
app.include_router(router_review)

@app.get("/",tags=["Root"])
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health",tags=["Root"])
def health_check():
    return {"status": "healthy"}