from sqlalchemy import Column, Integer, String, DateTime, Numeric
from .database import Base

class Route(Base):
    __tablename__ = "routes"

    id= Column(Integer , primary_key=True, index=True)
    origin= Column(String, nullable=False)
    destination= Column(String, nullable=False)
    departure_time= Column(DateTime, nullable=False)
    price= Column(Numeric(10,2), nullable=False)