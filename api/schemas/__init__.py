import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from api.model.base import Base

# Database directory and URL configuration
DB_PATH = "database/"
DB_URL = f'sqlite:///{DB_PATH}/patients.sqlite3'

# Ensure the database directory exists
os.makedirs(DB_PATH, exist_ok=True)

# Create the database engine
engine = create_engine(DB_URL, echo=False)

# Create a session factory bound to the engine
Session = sessionmaker(bind=engine)

# Create the database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

# Create all tables in the database if they don't exist
Base.metadata.create_all(engine)
