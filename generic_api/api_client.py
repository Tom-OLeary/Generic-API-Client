import backoff
import requests

from typing import Optional
from json import JSONDecodeError
from requests import HTTPError
from constants import API_USERNAME, API_PASSWORD
from generic_api.exceptions import AccessTokenException, backoff_expo_max_10, APIClientException, fatal_code, \
    APIRequestException


class APIClient:
    BASE_URL: str = "https://api.mock-endpoint.com/"
    AUTH_URL: str = BASE_URL + "user"
    POST = "POST"
    GET = "GET"

    access_token: Optional[str] = None

    def __init__(self):
        self.set_access_token()

    def set_access_token(self):
        response = requests.post(
            self.AUTH_URL,
            json={"username": API_USERNAME, "password": API_PASSWORD}
        )
        try:
            self.access_token = response.json()["token"]
        except (AttributeError, KeyError, JSONDecodeError):
            raise AccessTokenException(f"Failed to retrieve access token for user {API_USERNAME}")

    @backoff.on_exception(
        backoff_expo_max_10,
        APIClientException,
        max_tries=10,
        giveup=fatal_code,
    )
    def make_request(
            self,
            method: str,
            path: str = None,
            body: dict = None,
            url: str = None,
            query_params: dict = None,
    ) -> Optional[requests.Response]:
        """Sends API request to given path"""

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = url or self.BASE_URL + path

        try:
            if method == APIClient.POST:
                response = requests.post(url, headers=headers, params=query_params, json=body)
            elif method == APIClient.GET:
                response = requests.get(url, headers=headers, params=query_params)
            else:
                raise APIRequestException(f"Unsupported method for {method}. Choices are GET/POST")
        except HTTPError as e:
            raise APIClientException(e, self)

        response.raise_for_status()
        if response.status_code == 204:
            return

        return response

    def post_record(self, body: dict) -> Optional[requests.Response]:
        return self.make_request(
            method=APIClient.POST,
            path="records/createRecord",
            body=body,
        )

    def get_record(self, query_params: dict) -> Optional[requests.Response]:
        return self.make_request(
            method=APIClient.GET,
            path="records/recordNumber",
            query_params=query_params,
        )

