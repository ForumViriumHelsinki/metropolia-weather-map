from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from database.repositories import sensor_repo


class Coords(BaseModel):
    lon: float
    lat: float


class Sensor(BaseModel):
    id: str
    coords: Coords
    type
    note: str
    attached: str
    install_date: datetime


router = APIRouter()


@router.get("/api/sensors")
async def read_sensors():
    sensors = sensor_repo.get_sensors()
    print(sensors[0])
    return {"message": "hello"}
