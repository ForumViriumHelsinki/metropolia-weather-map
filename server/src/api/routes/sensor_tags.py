from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from api.models import SensorTag
from src.api.database import get_session

sensor_tag_router = APIRouter()


class DeleteTag(BaseModel):
    ids: List[str]
    tag: str


@sensor_tag_router.get("/api/sensor-tags")
def get_sensor_tags(session: Session = Depends(get_session)):
    try:
        statement = select(SensorTag)
        results = session.exec(statement)
        return results.all()

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching sensor tags: {str(e)}"
        )


@sensor_tag_router.delete("/api/sensor-tags")
def delete_tag_from_sensor(
    body: DeleteTag, session: Session = Depends(get_session)
):
    print(body)

    try:
        for sensor_id in body.ids:
            statement = (
                select(SensorTag)
                .where(SensorTag.sensor_id == sensor_id)
                .where(SensorTag.tag_id == body.tag)
            )
            result = session.exec(statement)
            valid_sensor_tag = result.first()

            if valid_sensor_tag:
                session.delete(valid_sensor_tag)

        session.commit()
        return "Sensor tags removed"

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting sensor tag: {str(e)}"
        )


class AddTag(BaseModel):
    ids: List[str]
    tag: str


@sensor_tag_router.post("/api/sensor-tags")
def add_tag_to_sensor(body: AddTag, session: Session = Depends(get_session)):
    try:
        for sensor in body.ids:
            existing_tag = session.exec(
                select(SensorTag).where(
                    (SensorTag.sensor_id == sensor)
                    & (SensorTag.tag_id == body.tag)
                )
            ).first()

            if not existing_tag:
                stmt = SensorTag(sensor_id=sensor, tag_id=body.tag)
                session.add(stmt)

        session.commit()
        return "Tags added"

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding tags: {str(e)}"
        )
