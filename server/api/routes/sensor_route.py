from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import sensor_table, sensordata_table, SensorDataInput

router = APIRouter()

@router.get("/api/sensors")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    qs = sensor_table.select()
    res = await db.execute(qs)
    sens = res.fetchall()
    return {"sensors": [dict(row._mapping) for row in sens]}
