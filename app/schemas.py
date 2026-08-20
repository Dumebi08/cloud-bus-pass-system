from datetime import datetime
from pydantic import BaseModel

class RouteResponse(BaseModel):  #creates  a pydantic model for the response of route
    id: int
    origin: str
    destination: str
    departure_time: datetime  
    price: float

    class Config:
        from_attributes = True # gives permission to pydantic to read data from the attributes of the SQLAlchemy model and convert it into a Pydantic model.
class BookingCreate(BaseModel):
    user_id: int
    route_id: int
    seat_id: int
   

    class Config:
        from_attributes = True
class BookingResponse(BookingCreate): # tells my FastAPi what API should return after a successful booking. It inherits from BookingCreate because the response will have the same fields as the request.
    id: int
    user_id: int
    seat_id: int
    ticket_id: str
    created_at: datetime

class TicketResponse(BaseModel):
    ticket_id: str
    passenger: str
    origin: str
    destination: str
    departure_time: datetime
    seat:str
    price: float
    status: str
    