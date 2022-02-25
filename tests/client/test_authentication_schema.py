from datetime import datetime
from datetime import timedelta

from faker import Faker

from instabd.schemas import Authentication

fake = Faker()


def test_expires_at():
    authentication = Authentication(
        access_token=fake.uuid4(),
        expires_in=3600,
    )

    expected_date = datetime.now() + timedelta(seconds=3600)
    assert authentication.expires_at.date() == expected_date.date()
    assert authentication.expires_at.second == expected_date.second
    assert authentication.expires_at.hour == expected_date.hour


def test_expires_at_null():
    authentication = Authentication(
        access_token=fake.uuid4(),
    )

    assert authentication.expires_at is None
