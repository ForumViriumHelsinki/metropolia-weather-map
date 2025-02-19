import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from tables import sensors

load_dotenv(".env.local")

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


def get_engine():
    url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url)
    return engine


def insert_sensor(sensor_data):
    engine = get_engine()
    with engine.connect() as conn:
        stmt = sensors.insert().values(sensor_data.to_dict())
        conn.execute(stmt)
        conn.commit()
