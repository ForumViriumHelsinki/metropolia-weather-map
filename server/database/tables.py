from sqlalchemy import Table, Column, MetaData, TEXT
from sqlalchemy.dialects.postgresql import DATE
from custom_types import Coords

metadata_obj = MetaData(schema="weather")

Sensors = Table(
    "sensors",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("coords", Coords()),
    Column("type", TEXT),
    Column("note", TEXT),
    Column("attached", TEXT),
    Column("install_date", DATE),
)
