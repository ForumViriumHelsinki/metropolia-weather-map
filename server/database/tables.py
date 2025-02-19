from sqlalchemy import Table, Column, MetaData, TypeDecorator, TEXT, Float
from sqlalchemy.dialects.postgresql import DATE, ENUM
from custom_types import Coords, TypeEnum

metadata_obj = MetaData(schema="weather_alt")

# asd = Coords()

sensors = Table(
    "sensors",
    metadata_obj,
    Column("id", TEXT, primary_key=True),
    Column("coords", Coords()),
    Column("type", ENUM(TypeEnum)),
    Column("note", TEXT),
    Column("attached", TEXT),
    Column("install_date", DATE),
)
