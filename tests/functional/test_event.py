from http import HTTPStatus
from urllib.parse import urljoin

import pytest

from tests.test_data.event import event_data, wrong_event_data
from tests.test_settings import test_settings

EVENT_ENDPOINT = "/api/v1/events/"
EVENT_URL = urljoin(test_settings.api_url, EVENT_ENDPOINT)

pytestmark = pytest.mark.asyncio


async def test_events_success(client_session, make_post_request):
    status, response = await make_post_request(EVENT_URL, event_data)
    assert status == HTTPStatus.NO_CONTENT


async def test_events_wrong(client_session, make_post_request):
    status, response = await make_post_request(EVENT_URL, wrong_event_data)
    assert status == HTTPStatus.UNPROCESSABLE_ENTITY
