from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import List, Optional
from datetime import datetime
from models import sensor_table, sensordata_table, SensorDataInput
from database import get_db
from routes.sensor_route import router as sensor_router

app = FastAPI()

app.include_router(sensor_router)


@app.get("/")
def home():
    return {"message": "Hello World"}

# Posts sensor data in batch to the database
@app.post("/api/sensordata/batch")
async def post_sensordata(
    data: List[SensorDataInput], db: AsyncSession = Depends(get_db)
):

    if not data:
        raise HTTPException(status_code=400, detail="Empty data list")

    sensor_ids = {entry.sensor for entry in data}

    result = await db.execute(
        select(sensor_table.c.id).where(sensor_table.c.id.in_(sensor_ids))
    )
    existing_sensors = {row[0] for row in result.fetchall()}

    valid_entries = []
    errors = []

    for entry in data:
        if entry.sensor in existing_sensors:
            valid_entries.append(
                {
                    "time": entry.time,
                    "humidity": entry.humidity,
                    "temperature": entry.temperature,
                    "sensor": entry.sensor,
                }
            )
        else:
            errors.append({"sensor": entry.sensor, "error": "Sensor ID not found"})

        if valid_entries:
            insert_stmt = sensordata_table.insert().values(valid_entries)
            try:
                await db.execute(insert_stmt)
                await db.commit()
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        return {
            "message": "Data inserted",
            "inserted": len(valid_entries),
            "Failed": errors,
        }

# Get sensors using any combination of filters
@app.get("/api/sensors/")
async def get_sensors(
    id : Optional[str] = Query(None),
    coords : Optional[str] = Query(None),
    type : Optional[str] = Query(None),
    note : Optional[str] = Query(None),
    attached : Optional[str] = Query(None),
    install_date_from : Optional[datetime] = Query(None),
    install_date_to : Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(sensor_table)
    filters = []
    if id:
        filters.append(sensor_table.c.id == id)

    if coords:
        filters.append(sensor_table.c.coords == coords)

    if type:
        filters.append(sensor_table.c.type == type)

    if note:
        filters.append(sensor_table.c.note == note)

    if attached:
        filters.append(sensor_table.c.attached == attached)

    if install_date_from:
        filters.append(sensor_table.c.install_date == install_date_from)

    if install_date_to:
        filters.append(sensor_table.c.install_date == install_date_to)

    if install_date_from and install_date_to and install_date_from > install_date_to:
        raise HTTPException(
            status_code=400, detail="install_date_from must be before install_date_to"
        )

    if filters:
        query = query.where(*filters)

    result = await db.execute(query)
    sensors = result.mappings().all()
    return {"sensors": [dict(row) for row in sensors]}

# Get sensor data using any combination of filters
@app.get("/api/sensordata/")
async def get_sensordata(
    sensor_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    humidity_from: Optional[float] = Query(None),
    humidity_to: Optional[float] = Query(None),
    temperature_from: Optional[float] = Query(None),
    temperature_to: Optional[float] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(sensordata_table)
    filters = []
    if sensor_id:
        filters.append(sensordata_table.c.sensor == sensor_id)

    if start_date:
        filters.append(sensordata_table.c.time >= start_date)

    if end_date:
        filters.append(sensordata_table.c.time <= end_date)

    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400, detail="start_date must be before end_date"
        )

    if humidity_from:
        if humidity_from < 0 or humidity_from > 100:
            raise HTTPException(
                status_code=400, detail="humidity value must be between 0 and 100"
            )
        else:
            filters.append(sensordata_table.c.humidity >= humidity_from)

    if humidity_to:
        if humidity_to < 0 or humidity_to > 100:
            raise HTTPException(
                status_code=400, detail="humidity value must be between 0 and 100"
            )
        else:
            filters.append(sensordata_table.c.humidity <= humidity_to)

    if humidity_from and humidity_to and humidity_from > humidity_to:
        raise HTTPException(
            status_code=400, detail="humidity_from must be less than humidity_to"
        )

    if temperature_from:
        filters.append(sensordata_table.c.temperature == temperature_from)

    if temperature_to:
        filters.append(sensordata_table.c.temperature == temperature_to)

    if temperature_from and temperature_to and temperature_from > temperature_to:
        raise HTTPException(
            status_code=400, detail="temperature_from must be less than temperature_to"
        )

    if filters:
        query = query.where(*filters)

    result = await db.execute(query)
    data = result.mappings().all()
    return {"data": [dict(row) for row in data]}
