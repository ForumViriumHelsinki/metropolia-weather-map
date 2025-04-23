from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.api.database import get_session
from src.api.models import Sensor, SensorTag

sensor_router = APIRouter()


@sensor_router.get("/api/sensors/")
def get_sensors(session: Session = Depends(get_session), tag: str | None = None):
    if tag:
        stmt = (
            select(Sensor)
            .join(SensorTag, Sensor.id == SensorTag.sensor_id)
            .where(SensorTag.tag_id == tag)
        )
    else:
        stmt = select(Sensor)

    try:
        sensors = session.exec(stmt).all()
        return sensors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
