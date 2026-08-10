from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:Dumebi2008%40@localhost:5432/cloud_bus_pass_system" #my database address

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

with engine.connect() as connection:  #used to establish and test my connection to the database
    print("Database connection established successfully!") 

Base = declarative_base()  #used to create the base class for my models

def get_db():
    db = SessionLocal()  # create a database session
    try:
        yield db  # gives the session to whoever calls this function or  needs it
    finally:
        db.close()  # close database session