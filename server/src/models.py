from typing import Optional
from sqlmodel import Field, SQLModel


class Sensor(SQLModel, table=True):
    id: str = Field(primary_key=True)
    coordinates: Optional[str]
    location: Optional[str]
    install_date: Optional[str]
    csv_link: Optional[str]


class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True)


class SensorTag(SQLModel, table=True):
    sensor_id: str = Field(foreign_key="sensor.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)
