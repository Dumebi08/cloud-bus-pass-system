from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint
from .database import Base

class Route(Base):
    __tablename__ = "routes"

    id= Column(Integer , primary_key=True, index=True)
    origin= Column(String, nullable=False)
    destination= Column(String, nullable=False)
    departure_time= Column(DateTime, nullable=False)
    price= Column(Numeric(10,2), nullable=False)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False, unique=True)
    ticket_id = Column(String(50), unique=True, nullable=False)
    status = Column(String(20), nullable=False, default="confirmed")
    created_at = Column(DateTime, nullable=False)

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    routes_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)

    __table_args__ = (
        UniqueConstraint('routes_id', 'seat_number', name='unique_seat_per_route'),
    )
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)