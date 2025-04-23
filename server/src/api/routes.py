from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from src.api.database import get_session
from src.api.models import Sensor, SensorTag, Tag

router = APIRouter()


@router.get("/api/sensors/")
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


@router.get("/api/tags")
def get_tags(session: Session = Depends(get_session)):
    try:
        tags = session.exec(select(Tag)).all()
        return tags
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.put("/api/tags")
def new_tag(new_tag: str, session: Session = Depends(get_session)):
    print(new_tag)
    try:
        tag_to_create = Tag(id=new_tag)
        ret = tag_to_create.model_copy()

        session.add(tag_to_create)
        session.commit()
        return ret
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
