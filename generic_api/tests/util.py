class MockResponse:
    def __init__(self, json_data: dict, status_code: int):
        self.json_data = json_data
        self.status_code = status_code
        self.text = "test response"

    def json(self):
        return self.json_data

    def raise_for_status(self):
        return


def mocked_requests_get(*args, **kwargs) -> MockResponse:
    end_path = args[0].split("/")[-1]
    if end_path == "recordNumber":
        return MockResponse(json_data={"recordNumber": "Record1"}, status_code=200)
    else:
        return MockResponse(json_data={}, status_code=200)


def mocked_requests_post(*args, **kwargs) -> MockResponse:
    end_path = args[0].split("/")[-1] if args else kwargs.get("url", "")
    if "createRecord" in end_path:
        return MockResponse(json_data=kwargs.get("json", {}), status_code=200)
    elif end_path == "user":
        return MockResponse(json_data={"token": "user_token"}, status_code=200)
    else:
        return MockResponse(json_data={}, status_code=200)



