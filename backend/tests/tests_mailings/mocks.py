class FackeResponse:
    def __init__(self, status):
        self._status = status

    @property
    def ok(self):
        return self._status

    def json(self):
        if self._status:
            return {"code": 0, "message": "OK"}

        return {"code": 0, "message": "Error"}


def fake_requests_post(service_url, headers, data) -> FackeResponse:
    if not hasattr("fake_requests_post", "status"):
        fake_requests_post.status = True
    return FackeResponse(fake_requests_post.status)


def fake_check_time():
    return True
