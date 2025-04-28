from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from src.analysis.scripts.temperature_by_tag import temperature_by_tag
from src.api.database import get_session
from src.api.models import Sensor, SensorTag

analysis_router = APIRouter()


@analysis_router.get("/api/analysis/temperature")
def get_temperature_graph():
    result = temperature_by_tag(
        tag1="aurinko",
        tag2="varjo",
        location="Vallila",
        graph_type="plot",
        start_date=None,
        end_date=None,
        daytime=False,
        nighttime=False,
    )

    return type(result)
    return "not implemented"
