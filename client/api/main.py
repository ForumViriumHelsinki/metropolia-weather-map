from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from geoalchemy2 import Geometry
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://postgres:pass@localhost:5432/weatherdb"

#Set up of async engine
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

#Defining ORM models for the database
class Sensor(Base):
   __tablename__ = "sensors"
   __table_args__ = {"schema": "weather"}

   id = Column(String, primary_key=True, index=True)
   location = Column(Geometry("POINT"))
   type = Column(String)
   note = Column(String)
   attached = Column(String)
   install_date = Column(Date)

class SensorData(Base):
    __tablename__ = "sensordata"
    __table_args__ = {"schema": "weather"}

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime)
    humidity = Column(Float)
    temperature = Column(Float)
    sensor = Column(String)

#Creating fastapi instance
app = FastAPI()

#Dependency for getting the session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    query = text("SELECT id, location, type, note, attached, install_date FROM weather.sensors")
    result = await db.execute(query)
    sensors = result.fetchall()
    return {"sensors": [dict(row._mapping) for row in sensors]}

@app.get("/api/sensors/{sensor_id}")
async def get_sensor(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = text("SELECT id, location, type, note, attached, install_date FROM weather.sensors WHERE id = :sensor_id")
    result = await db.execute(query, {"sensor_id": sensor_id})
    sensor = result.fetchone()
    return {"sensor": dict(sensor._mapping)}

@app.get("/api/sensors/{sensor_id}/data")
async def get_sensor_data(sensor_id: str, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM weather.sensordata WHERE sensor = :sensor_id")
    result = await db.execute(query, {"sensor_id": sensor_id})
    data = result.fetchall()
    return {"data": [dict(row._mapping) for row in data]}
