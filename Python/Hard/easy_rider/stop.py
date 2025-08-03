import re
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Stop:
    bus_id: int
    stop_id: int
    stop_name: str
    next_stop: int
    stop_type: str
    a_time: str

    EXPECTED_DATA = [
        ('bus_id', 'int', 1),
        ('stop_id', 'int', 1),
        ('stop_name', 'str', 1),
        ('next_stop', 'int', 1),
        ('stop_type', 'str', 0),
        ('a_time', 'str', 1)
    ]

    EXPECTED_FORMAT = {
        'stop_name': re.compile(
            "([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$"),
        'stop_type': re.compile("(S|O|F)?$"),
        'a_time': re.compile("([01][0-9]|2[0-4]):[0-5][0-9]$")
    }

    class InvalidData(Exception):
        def __init__(self, field, *args: object) -> None:
            super().__init__(*args)
            self.field = field

    class InvalidFormat(Exception):
        def __init__(self, field, *args: object) -> None:
            super().__init__(*args)
            self.field = field

    @classmethod
    def from_dict(cls, obj: dict) -> 'Stop':
        for field, field_type, required in cls.EXPECTED_DATA:
            if field not in obj:
                raise cls.InvalidData(field)
            if required and not str(obj[field]):
                raise cls.InvalidData(field)
            if not isinstance(obj[field], eval(field_type)):
                raise cls.InvalidData(field)
            if (field in cls.EXPECTED_FORMAT
                    and not cls.EXPECTED_FORMAT[field].match(obj[field])):
                raise cls.InvalidFormat(field)
        return cls(**obj)

    @property
    def arr_time(self) -> datetime:
        return datetime.strptime(self.a_time, "%H:%M")
