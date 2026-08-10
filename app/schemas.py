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