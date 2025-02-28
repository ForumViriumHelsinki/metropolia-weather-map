import os, sys

sys.path.append("./database")
sys.path.append("./routers")

from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from routers import sensors

app = FastAPI()

app.include_router(sensors.router)


class DateRange(BaseModel):
    startDate: datetime
    endDate: datetime


@app.get("/")
def root():
    return {"Message": "hello"}


# Get data by date range
@app.get("/api/data/date")
def get_data_by_date(dates: DateRange):
    startDate = dates.startDate
    endDate = dates.endDate

    return {"Message": "Hello"}
