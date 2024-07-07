from enum import Enum
from typing import Optional

from generic_api.api_client import APIClient
from generic_api.exceptions import RequestHandlerException, APIRequestException
from generic_api.validation import PostRecord, GetRecord


class RequestEnum(Enum):
    POST_RECORD = (
        "POST_RECORD",
        "post_record",
        PostRecord,
    )
    GET_RECORD = (
        "GET_RECORD",
        "get_record",
        GetRecord,
    )

    @property
    def trigger(self):
        return self.value[0]

    @property
    def api_method(self):
        return self.value[1]

    @property
    def format(self):
        return self.value[2]

    @classmethod
    def valid_triggers(cls):
        return [key.trigger for key in cls]


class RequestHandler:
    def __init__(self, trigger: str, body: dict):
        if not all([trigger, body]):
            raise RequestHandlerException(f"trigger: {trigger} and body: {body} cannot be None")

        self.trigger = trigger.upper()
        self.body = body
        self.api = APIClient()

        try:
            self.request = RequestEnum[self.trigger]
            self.format_object = self.request.format(**self.body)
        except KeyError:
            raise RequestHandlerException(f"Unsupported trigger: {trigger}. Valid options are {RequestEnum.valid_triggers()}")
        except TypeError as e:
            # missing fields or invalid types during formatting
            raise RequestHandlerException(str(e))

    def handle_request(self) -> Optional[dict]:
        try:
            response = getattr(self.api, self.request.api_method)(**self.format_object.request_body)
        except APIRequestException as e:
            raise RequestHandlerException from e

        if response is None:
            return

        return {"status_code": response.status_code, "data": response.json()}

