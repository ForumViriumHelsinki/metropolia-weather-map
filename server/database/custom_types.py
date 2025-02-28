from sqlalchemy.types import UserDefinedType


class Sensor:
    def __init__(self, id, coords, type, note, attached, install_date):
        self.id = id
        self.coords = coords
        self.type = type
        self.note = note
        self.attached = attached
        self.install_date = install_date

    def to_dict(self):
        return {
            "id": self.id,
            "coords": self.coords,
            "type": self.type,
            "note": self.note,
            "attached": self.attached,
            "install_date": self.install_date,
        }

    def __str__(self):
        return f"Sensor(id={self.id}, coords={self.coords}, type={self.type}, note={self.note}, attached={self.attached}, install_date={self.install_date})"


class Coords(UserDefinedType):

    def get_col_spec(self):
        return "coords"

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return f"({value[0]}, {value[1]})"
            return value

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return tuple(map(float, value[1:-1].split(",")))
            return value

        return process
