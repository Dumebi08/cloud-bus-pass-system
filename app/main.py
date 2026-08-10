from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Route 
from .schemas import RouteResponse

app = FastAPI()  #application object

@app.get("/")
def home():
    return {"message": "Cloud Bus Pass System is running!"}

@app.get("/routes", response_model= list[RouteResponse]) # tells it to return of routeresponse objects
def get_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    
    return routes