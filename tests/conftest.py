import pytest
from faker import Faker

from client import InstagramBasicDisplayClient
from client import UserClient
from schemas import Authentication
from schemas import Children
from schemas import Media

fake = Faker()


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def client():
    return InstagramBasicDisplayClient(
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
