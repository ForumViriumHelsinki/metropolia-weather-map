from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from src.api.database import get_session
from src.api.models import Sensor

router = APIRouter()


@router.get("/api/sensors/")
def get_sensors(session: Session = Depends(get_session)):
    try:
        sensors = session.exec(select(Sensor)).all()
        return sensors
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
