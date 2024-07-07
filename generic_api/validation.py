import datetime
from dataclasses import dataclass, fields, MISSING


@dataclass
class GetRecord:
    record_number: str

    @property
    def request_body(self):
        return {
            "query_params": {
                "recordNumber": self.record_number
            }
        }


@dataclass
class PostRecord:
    required_str: str
    required_int: int
    required_float: float

    optional_str1: str = None
    optional_str2: str = None
    optional_datetime: datetime = None
    optional_list: list = None
    optional_dict: dict = None

    def __post_init__(self):
        validation_errors = []
        for f in fields(self):
            try:
                self.validate_type(f)
            except TypeError as e:
                validation_errors.append(e)

    def validate_type(self, f: any):
        if not getattr(self, f.name):
            if f.default is not MISSING:
                _default = f.default or empty_field(f.type)
                setattr(self, f.name, _default)
            else:
                raise TypeError(f"Required field {f.name} cannot be None")

        # recall getattr here in case field changes to new/default value
        _value_type = type(getattr(self, f.name))
        if not isinstance(f.type, _value_type):
            raise TypeError(f"Invalid type for {f.name} {f.type}. Failing value type is {_value_type}")


def empty_field(f_type: any):
    if isinstance(f_type, str):
        return ""
    elif isinstance(f_type, bool):
        return False
    elif isinstance(f_type, int):
        return 0
    elif isinstance(f_type, float):
        return 0.0

