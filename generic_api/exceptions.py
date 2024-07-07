import json
from http.client import RemoteDisconnected

import backoff
from json import JSONDecodeError
from typing import Union, Generator

from requests import HTTPError
from requests.exceptions import SSLError


class AccessTokenException(Exception):
    pass


class APIRequestException(Exception):
    pass


class RequestHandlerException(Exception):
    pass


class APIClientException(Exception):
    def __init__(self, source: Union[Exception, HTTPError], api: any):
        self.source = source
        self.api = api

    def get_context(self):
        exc_str = self.source.response.context.decode("utf-8")
        try:
            return json.loads(exc_str)
        except JSONDecodeError:
            return {"details": exc_str}

    def get_headers(self):
        try:
            return self.source.response.headers.decode("utf-8")
        except AttributeError:
            return

    def __str__(self):
        return str(self.source)


def backoff_expo_max_10() -> Generator:
    return backoff.expo(max_value=10)


def fatal_code(e: APIClientException) -> bool:
    status_code = e.source.response.status_code
    if isinstance(e.source, (RemoteDisconnected, SSLError)) or status_code == 401:
        e.api.set_access_token()
        return False

    return status_code not in (429, 500, 503) and not (200 <= status_code < 300)
