import io
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from src.analysis.scripts.temperature_by_tag import temperature_by_tag
from src.api.database import get_session
from src.api.models import Sensor, SensorTag
from starlette.responses import StreamingResponse

analysis_router = APIRouter()


@analysis_router.get("/api/analysis/temperature")
def get_temperature_graph():
    graph = temperature_by_tag(
        tag1="aurinko",
        tag2="varjo",
        location="Vallila",
        graph_type="plot",
        start_date=None,
        end_date=None,
        daytime=False,
        nighttime=False,
    )

    buf = io.BytesIO()
    graph.savefig(buf, format="svg")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/svg+xml")
