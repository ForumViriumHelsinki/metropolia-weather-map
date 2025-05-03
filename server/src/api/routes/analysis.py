import calendar
import io
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from src.analysis.scripts.temperature_by_tag import temperature_by_tag
from starlette.responses import StreamingResponse

analysis_router = APIRouter()


@analysis_router.get("/api/analysis/temperature")
def get_temperature_graph(
    tag1: str,
    tag2: str,
    graph_type: str,
    location: str = None,
    start_date: str = None,
    end_date: str = None,
    daytime: bool = False,
    nighttime: bool = False,
):
    print("/analysis/temperature GET")
    print(
        f"tag1: {tag1}, tag2: {tag2}, location: {location}, graph_type: {graph_type}, "
        f"start_date: {start_date}, end_date: {end_date}, daytime: {daytime}, nighttime: {nighttime}"
    )

    if graph_type == "bar" and start_date and end_date:
        # Parse start date
        year, month = start_date.split("-")
        start_date = date(year=int(year), month=int(month), day=1)

        # Parse end date
        year, month = map(int, end_date.split("-"))
        last_day = calendar.monthrange(year, month)[1]
        end_date = date(year=year, month=month, day=last_day)

    try:
        graph = temperature_by_tag(
            tag1=tag1,
            tag2=tag2,
            location=location,
            graph_type=graph_type,
            start_date=start_date,
            end_date=end_date,
            daytime=daytime,
            nighttime=nighttime,
        )

        buf = io.BytesIO()
        graph.savefig(buf, format="svg")
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/svg+xml")
    except Exception as e:
        print(e)
