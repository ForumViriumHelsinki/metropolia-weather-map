from tables import Sensors
from ..db import get_connection


def get_sensors():
    with get_connection() as conn:
        res = conn.execute(Sensors.select())
        sensors = res.fetchall()
        return sensors
