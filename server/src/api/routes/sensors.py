from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from api.database import get_session
from api.models import Sensor, SensorTag

sensor_router = APIRouter()


@sensor_router.get("/api/sensors")
def get_sensors(
    session: Session = Depends(get_session), tag: str | None = None
):
    if tag:
        stmt = (
            select(Sensor)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
    else:
        stmt = select(Sensor)

    try:
        return session.exec(stmt).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class NewSensor(BaseModel):
    id: str
    lat: float
    lon: float
    location: str
    install_date: date
    csv_link: str


@sensor_router.post("/api/sensors")
def add_sensor(session: Session = Depends(get_session)):
    return "Not implemented"
