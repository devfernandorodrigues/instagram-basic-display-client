import pytest
from faker import Faker

from instabd.client import InstabdClient
from instabd.request import request
from instabd.schemas import Authentication
from instabd.schemas import Children
from instabd.schemas import Media
from instabd.user_client import UserClient

fake = Faker()


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def req():
    return request


@pytest.fixture
def client():
    return InstabdClient(
        client_id=fake.uuid4(),
        client_secret=fake.uuid4(),
        redirect_uri=fake.url(),
    )


@pytest.fixture
def user_client():
    return UserClient(
        authentication=Authentication(
            access_token=fake.uuid4(),
        )
    )


@pytest.fixture
def media():
    return Media(
        id=fake.uuid4(),
        caption=fake.pystr(),
        media_type=fake.pystr(),
        media_url=fake.url(),
        permalink=fake.url(),
        thumbnail_url=fake.url(),
        timestamp=fake.date_time().isoformat(),
        username=fake.user_name(),
    )


@pytest.fixture
def children():
    return Children(
        id=fake.uuid4(),
        caption=fake.pystr(),
        media_type=fake.pystr(),
        media_url=fake.url(),
        permalink=fake.url(),
        thumbnail_url=fake.url(),
        timestamp=fake.date_time().isoformat(),
        username=fake.user_name(),
    )


@pytest.fixture
def error():
    return {
        "error": {
            "message": "...",
            "type": "IGApiException",
            "code": 100,
            "error_subcode": 33,
            "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
        }
    }
