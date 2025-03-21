from sqlalchemy import MetaData
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Optional


meta = MetaData(schema="weather")

engine = create_async_engine(
    "postgresql+asyncpg://postgres:pass@host.docker.internal:5432/weatherdb", echo=True
)


class Sensors(SQLModel, table=True):
    metadata = meta
    id: str = Field(primary_key=True)
    coordinates: Optional[str]
    location: Optional[str]
    install_date: Optional[str]
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
