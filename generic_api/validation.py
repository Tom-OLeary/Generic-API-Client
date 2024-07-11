import datetime
from dataclasses import dataclass, fields, MISSING


@dataclass
class GetRecord:
    record_number: str

    @property
    def request_body(self):
        return {"query_params": {"recordNumber": self.record_number}}


@dataclass
class PostRecord:
    required_str: str
    required_int: int
    required_float: float

    optional_str1: str = None
    optional_str2: str = None
    optional_datetime: str = None
    optional_list: list = None
    optional_dict: dict = None

    def __post_init__(self):
        validation_errors = []
        for f in fields(self):
            try:
                self.validate_type(f)
            except TypeError as e:
                validation_errors.append(e)

        if validation_errors:
            raise TypeError(f"{len(validation_errors)} validation errors occurred. Errors {validation_errors}")

    def validate_type(self, f: any):
        if not getattr(self, f.name):
            if f.default is not MISSING:
                _default = f.default or empty_field(f.type)
                setattr(self, f.name, _default)
            else:
                raise TypeError(f"Required field {f.name} cannot be None")

        # recall getattr here in case field changes to new/default value
        _value_type = type(getattr(self, f.name))
        if f.type is not _value_type:
            raise TypeError(f"Invalid type for {f.name} {f.type}. Failing value type is {_value_type}")

    @property
    def request_body(self):
        return {"body": {f.name: getattr(self, f.name) for f in fields(self)}}


def empty_field(f_type: any):
    if f_type is str:
        return ""
    elif f_type is bool:
        return False
    elif f_type is int:
        return 0
    elif f_type is float:
        return 0.0
    elif f_type is list:
        return []
    elif f_type is dict:
        return {}

