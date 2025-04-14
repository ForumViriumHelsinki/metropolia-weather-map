from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Sensor(SQLModel, table=True):
    __tablename__ = "sensors"
    __table_args__ = {"schema": "weather"}

    id: str = Field(default=None, primary_key=True)
    coordinates: Optional[str] = Field(default=None)  # Use string to represent 'point'
    location: Optional[str] = None
    install_date: Optional[date] = None
    csv_link: Optional[str] = None

    tags: List["SensorTag"] = Relationship(
        back_populates="sensor"
    )  # Define relationship


class Tag(SQLModel, table=True):
    __tablename__ = "tags"
    __table_args__ = {"schema": "weather"}

    id: str = Field(primary_key=True)

    sensors: List["SensorTag"] = Relationship(
        back_populates="tag"
    )  # Define relationship


class SensorTag(SQLModel, table=True):
    __tablename__ = "sensor_tags"
    __table_args__ = {"schema": "weather"}

    sensor_id: str = Field(foreign_key="weather.sensors.id", primary_key=True)
    tag_id: str = Field(foreign_key="weather.tags.id", primary_key=True)

    sensor: "Sensor" = Relationship(back_populates="tags")  # Define relationship
    tag: "Tag" = Relationship(back_populates="sensors")  # Define relationship
