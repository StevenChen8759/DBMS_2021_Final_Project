
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_string = "postgresql://postgres:stevenchen@10.8.3.200:5432/sim"

def connect():
    db = create_engine(db_string)
    Session = sessionmaker(db)
    return Session()

def disconnect(session):
    session.close()