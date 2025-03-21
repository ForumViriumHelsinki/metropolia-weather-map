from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import date

class Sensor(SQLModel, table=True):
    __tablename__ = "sensors"
    __table_args__ = {"schema": "weather"}  # Specify the schema

    id: str = Field(default=None, primary_key=True)
    coordinates: Optional[str] = None
    location: Optional[str] = None
    install_date: Optional[date] = None
    csv_link: Optional[str] = None

class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True)


class SensorTag(SQLModel, table=True):
    sensor_id: str = Field(foreign_key="sensor.id", primary_key=True)
    tag_id: str = Field(foreign_key="tag.id", primary_key=True)
