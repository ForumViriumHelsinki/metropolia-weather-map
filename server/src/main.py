import sys
import os
from fastapi import FastAPI
from .sensor_repo import get_sensors  # Use relative import

app = FastAPI()


@app.get("/")
def home():
    return {"Hello"}


@app.get("/api/sensors")
async def test_get():
    sensors = await get_sensors()
    return sensors
