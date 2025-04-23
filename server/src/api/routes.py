from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
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


class DeleteTag(BaseModel):
    sensor_id: str
    tag: str


@router.delete("/api/sensor-tags")
def delete_tag_from_sensor(body: DeleteTag, session: Session = Depends(get_session)):
    print(body)
    try:
        statement = (
            select(SensorTag)
            .where(SensorTag.sensor_id == body.sensor_id)
            .where(SensorTag.tag_id == body.tag)
        )
        result = session.exec(statement)
        sensor_tag = result.one()
        print(sensor_tag)

        session.delete(sensor_tag)
        session.commit()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting sensor tag: {str(e)}"
        )

    return "not done"


class AddTag(BaseModel):
    ids: List[str]
    tag: str


@router.post("/api/sensor-tags")
def add_tag_to_sensor(body: AddTag, session: Session = Depends(get_session)):
    try:
        for sensor in body.ids:
            stmt = SensorTag(sensor_id=sensor, tag_id=body.tag)
            session.add(stmt)
        session.commit()
        return "Tags added"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding tags: {str(e)}")


@router.get("/api/tags")
def get_tags(session: Session = Depends(get_session)):
    try:
        tags = session.exec(select(Tag)).all()
        return tags
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("/api/tags")
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
