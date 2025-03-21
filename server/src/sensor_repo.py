import os
from datetime import date
from typing import NamedTuple, Optional, Tuple

from sqlalchemy import Column, String
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Column, Field, MetaData, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


class Point(NamedTuple):
    x: float
    y: float


import os

meta = MetaData(schema="weather")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "pass")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weatherdb")


engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=True
)


class Sensors(SQLModel, table=True):
    metadata = meta
    id: str = Field(primary_key=True)
    coordinates: Optional[Point] = Field(sa_column=Column(String))
    location: Optional[str]
    install_date: Optional[date]
    csv_link: Optional[str]


class Tag(SQLModel, table=True):
    metadata = meta
    id: str = Field(primary_key=True)


class SensorTag(SQLModel, table=True):
    metadata = meta
    sensor_id: str = Field(foreign_key="sensor.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)


async def get_sensors():
    async with AsyncSession(engine) as session:
        statement = select(Sensors)
        result = await session.exec(statement)
        sensors = result.all()
        return sensors
