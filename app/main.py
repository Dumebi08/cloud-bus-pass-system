from fastapi import FastAPI 

app = FastAPI()  #application object

@app.get("/")
def home():
    return {"message": "Cloud Bus Pass System is running!"}

@app.post("/bookings")
def create_booking():
    return {"message": "Booking created successfully!"}