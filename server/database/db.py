import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env.local file
load_dotenv("../.env.local")

# Retrieve database connection details from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Construct the database URL
url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(url)


def get_connection():
    try:
        connection = engine.connect()
        return connection
    except SQLAlchemyError as e:
        print(f"Error connecting to the database: {e}")
        return None
