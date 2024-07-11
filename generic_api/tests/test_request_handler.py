from unittest import mock, TestCase

from generic_api.request_handler import RequestEnum, RequestHandler
from generic_api.tests.util import mocked_requests_post, mocked_requests_get


@mock.patch("requests.post", side_effect=mocked_requests_post)
def test_create_record(mock_post):
    post_data = {
        "required_str": "required1",
        "required_int": 2,
        "required_float": 45.0,
        "optional_str1": "",
        "optional_str2": "",
        "optional_datetime": "",
        "optional_list": [],
        "optional_dict": {},
    }
    trigger = "post_record"
    handler = RequestHandler(trigger=trigger, body=post_data)
    response = handler.handle_request()
    assert response["status_code"] == 200
    for key, value in post_data.items():
        assert response["data"][key] == value


@mock.patch("requests.post", side_effect=mocked_requests_post)
@mock.patch("requests.get", side_effect=mocked_requests_get)
def test_create_record(mock_get, mock_post):
    body = {"record_number": "Record1"}
    trigger = "get_record"
    handler = RequestHandler(trigger=trigger, body=body)
    response = handler.handle_request()
    assert response["status_code"] == 200
    assert response["data"]["recordNumber"] == body["record_number"]

