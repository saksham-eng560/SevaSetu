from sqlmodel import create_engine, SQLModel, Session
from models.booking import Booking
from models.customer import Customer
from models.provider import Provider
from models.review import Review

DATABASE_URL = "sqlite:///./seva_setu.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session