from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Date, select
from geoalchemy2 import Geometry
from sqlalchemy import text
from sqlalchemy import Table, Column, MetaData, TEXT, DATETIME
from sqlalchemy.dialects.postgresql import DATE
from datetime import datetime
from dateutil import parser
from pydantic import BaseModel, Field
from typing import List
DATABASE_URL = "postgresql+asyncpg://postgres:pass@localhost:5432/weather"

#Set up of async engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

metadata_obj = MetaData(schema="weather")

sensor_table = Table(
    "sensors",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("coords", TEXT),
    Column("type", TEXT),
    Column("note", TEXT),
    Column("attached", TEXT),
    Column("install_date", DATE),
)

sensordata_table = Table(
    "sensordata",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("time", TIMESTAMP),
    Column("humidity", TEXT),
    Column("temperature", TEXT),
    Column("sensor", TEXT),
)

app = FastAPI()

class SensorDataInput(BaseModel):
    time: datetime
    humidity: float = Field(..., ge=0, le=100)  # Humidity must be between 0-100%
    temperature: float
    sensor: str  # Sensor ID must match an existing sensor

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    qs = sensor_table.select()

    res = await db.execute(qs)

    sens = res.fetchall()

    return {"sensors": [dict(row._mapping) for row in sens]}


#Dependency for getting the session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.post("/api/sensordata/batch")
async def post_sensordata(data: List[SensorDataInput], db: AsyncSession = Depends(get_db)):
    
    if not data:
        raise HTTPException(status_code=400, detail="Empty data list")
    
    sensor_ids = {entry.sensor for entry in data}
    
    result = await db.execute(select(sensor_table.c.id).where(sensor_table.c.id.in_(sensor_ids)))
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
                    "sensor": entry.sensor
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
            "Failed": errors
        }
    

@app.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    query = sensor_table.select()
    result = await db.execute(query)
    sensors = result.fetchall()
    return {"sensors": [dict(row._mapping) for row in sensors]}

@app.get("/api/sensors/{sensor_id}")
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = sensor_table.select().where(sensor_table.c.id == sensor_id)
    result = await db.execute(query)
    sensor = result.fetchone()
    return {"sensor": dict(sensor._mapping)}

@app.get("/api/sensordata/{sensor_id}")
async def get_sensor_data(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = sensordata_table.select().where(sensordata_table.c.sensor == sensor_id)
    result = await db.execute(query)
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}

@app.get("/api/sensordata/{start_date}/{end_date}")
async def get_sensor_data_range(start_date: str, end_date: str, db: AsyncSession = Depends(get_db)):

    try:
        start_dt = parser.isoparse(start_date).replace(tzinfo=None)
        end_dt = parser.isoparse(end_date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    if start_dt > end_dt:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")

    query = sensor_table.select().where(sensordata_table.c.time.between(start_dt, end_dt))
    result = await db.execute(query, {"start_date": start_dt, "end_date": end_dt})
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}

@app.get("/api/sensors/type/{type}")
async def get_sensor(type: str, db: AsyncSession = Depends(get_db)):
    query = sensor_table.select().where(sensor_table.c.type == type)
    result = await db.execute(query)
    sensors = result.fetchall()
    return {"sensors": [dict(row._mapping) for row in sensors]}

@app.get("/api/sensordata/temperature/greater/{temp}")
async def get_sensordata(temp: float, db: AsyncSession = Depends(get_db)):
    query = sensordata_table.select().where(sensordata_table.c.temperature > temp)
    result = await db.execute(query)
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}

@app.get("/api/sensordata/temperature/less/{temp}")
async def get_sensordata(temp: float, db: AsyncSession = Depends(get_db)):
    query = sensordata_table.select().where(sensordata_table.c.temperature < temp)
    result = await db.execute(query)
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}

@app.get("/api/sensordata/humidity/greater/{hum}")
async def get_sensordata(hum: float, db: AsyncSession = Depends(get_db)):
    query = sensordata_table.select().where(sensordata_table.c.humidity > hum)
    result = await db.execute(query)
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}

@app.get("/api/sensordata/humidity/less/{hum}")
async def get_sensordata(hum: float, db: AsyncSession = Depends(get_db)):
    query = sensordata_table.select().where(sensordata_table.c.humidity < hum)
    result = await db.execute(query)
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}