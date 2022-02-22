import pytest
from faker import Faker

from client import InstagramBasicDisplayClient
from client import UserClient
from schemas import Authentication

fake = Faker()


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
