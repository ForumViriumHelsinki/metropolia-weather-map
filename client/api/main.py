from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import TIMESTAMP, Column, text, Table, MetaData, TEXT
from sqlalchemy.dialects.postgresql import DATE
from datetime import datetime

DATABASE_URL = "postgresql+asyncpg://postgres:pass@localhost:5432/weather"

# Set up of async engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

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


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    qs = sensor_table.select()

    res = await db.execute(qs)

    sens = res.fetchall()

    return {"sensors": [dict(row._mapping) for row in sens]}


# Creating fastapi instance
app = FastAPI()


# Dependency for getting the session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/")
def home():
    return {"message": "Hello World"}


@app.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    query = text(
        "SELECT id, coords, type, note, attached, install_date FROM weather.sensors"
    )
    result = await db.execute(query)
    sensors = result.fetchall()
    return {"sensors": [dict(row._mapping) for row in sensors]}


@app.get("/api/sensors/id/{sensor_id}")
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = text(
        "SELECT id, coords, type, note, attached, install_date FROM weather.sensors WHERE id = :sensor_id"
    )
    result = await db.execute(query, {"sensor_id": sensor_id})
    sensor = result.fetchone()
    return {"sensor": dict(sensor._mapping)}


@app.get("/api/sensordata/id/{sensor_id}")
async def get_sensor_data(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM weather.sensordata WHERE sensor = :sensor_id")
    result = await db.execute(query, {"sensor_id": sensor_id})
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}


@app.get("/api/sensordata/dates")
async def get_sensor_data_range(
    start_date: str, end_date: str, db: AsyncSession = Depends(get_db)
):

    try:
        # Fix date format
        start_date = start_date.replace(" ", "+")
        end_date = end_date.replace(" ", "+")

        start_dt = datetime.fromisoformat(start_date).replace(tzinfo=None)
        end_dt = datetime.fromisoformat(end_date).replace(tzinfo=None)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    if start_dt > end_dt:
        raise HTTPException(
            status_code=400, detail="start_date must be before end_date"
        )

    query = sensordata_table.select().where(
        sensordata_table.c.time.between(start_dt, end_dt)
    )
    result = await db.execute(query, {"start_date": start_dt, "end_date": end_dt})
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}


@app.get("/api/sensors/type/{type}")
async def add_sensor(type: str, db: AsyncSession = Depends(get_db)):
    print({"type": type})

    query = sensor_table.select().where(sensor_table.c.type == type)
    result = await db.execute(query)
    sensors = result.fetchall()
    return {"sensors": [dict(row._mapping) for row in sensors]}
