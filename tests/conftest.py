import pytest
from faker import Faker

from client import InstagramBasicDisplayClient

fake = Faker()


@pytest.fixture
def client():
    return InstagramBasicDisplayClient(
        client_id=fake.uuid4(),
        client_secret=fake.uuid4(),
        redirect_uri=fake.url(),
    )
