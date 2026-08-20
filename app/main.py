import secrets
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from .database import get_db, Base, engine
from .models import Route , Seat, Booking, User 
from .schemas import RouteResponse, BookingCreate, BookingResponse, TicketResponse
from . import models

app = FastAPI()  #application object

@app.get("/")
def home():
    return {"message": "Cloud Bus Pass System is running!"}

Base.metadata.create_all(bind=engine)  #creates the tables in the database if they don't exist

@app.get("/routes", response_model= list[RouteResponse]) # tells it to return of routeresponse objects
def get_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    
    return routes

@app.post("/bookings")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.id == booking.user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #checks if the seat is already booked
    seat = db.query(Seat).filter(  
       Seat.id == booking.seat_id
    ).first()

    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")

    existing_booking = db.query(Booking).filter(
        Booking.seat_id == booking.seat_id,
        Booking.route_id == booking.route_id
    ).first()

    if existing_booking:
        raise HTTPException(status_code=409, detail="Seat already booked")

    ticket_id = "TKT-"+ secrets.token_hex(8).upper() # my booking object that generates a random ticket id
    new_booking= Booking(
        user_id= booking.user_id,
        seat_id= booking.seat_id,
        route_id= booking.route_id,
        ticket_id= ticket_id,
        status= "confirmed",
        created_at= datetime.now()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return booking

@app.get("/bookings/{ticket_id}", response_model= TicketResponse)
def get_booking(ticket_id: str, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(
        Booking.ticket_id == ticket_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    user = db.query(User).filter(
        User.id == booking.user_id
    ).first()
    route = db.query(Route).filter(
        Route.id == booking.route_id
    ).first()   
    seat = db.query(Seat).filter(
        Seat.id == booking.seat_id
    ).first()

    return {
        "ticket_id": booking.ticket_id,
        "passenger": user.name,
        "origin": route.origin,
        "destination": route.destination,
        "departure_time": route.departure_time,
        "seat": seat.seat_number, 
        "price": float(route.price),
        "status": booking.status
    }
    
@app.patch("/bookings/{ticket_id}/cancel")
def cancel_booking(ticket_id: str, db :Session = Depends(get_db)):
    booking = db.query(Booking).filter(
        Booking.ticket_id == ticket_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")

    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return{
        "message": "Booking cancelled successfully",
        "ticket_id": booking.ticket_id,
        "status": booking.status
    }