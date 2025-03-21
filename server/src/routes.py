from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import get_db
from .models import Sensor

router = APIRouter()

@router.get("/api/sensors/")
async def get_sensors(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Sensor))
        sensors = result.scalars().all()
        return {"data": sensors}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


