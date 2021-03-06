import pytest
import responses
from faker import Faker
from responses import matchers

from instabd.exceptions import IGApiException
from instabd.schemas import Authentication

fake = Faker()

URL = "https://graph.instagram.com/access_token"


@responses.activate
def test_call(client):
    access_token = fake.uuid4()
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": client.client_secret,
        "access_token": access_token,
    }
    responses.add(
        responses.GET,
        URL,
        json={"access_token": access_token, "expires_in": 5183944},
        match=[matchers.query_param_matcher(params)],
    )

    client.long_lived_token(access_token)

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_response(client):
    access_token = fake.uuid4()
    responses.add(
        responses.GET,
        URL,
        json={"access_token": access_token, "expires_in": 5183944},
    )

    authentication = client.long_lived_token(fake.uuid4())

    assert authentication.access_token == access_token
    assert authentication.expires_at is not None


@responses.activate
def test_instance(client):
    responses.add(
        responses.GET,
        URL,
        json={"access_token": fake.uuid4()},
    )

    authentication = client.long_lived_token(fake.uuid4())

    assert isinstance(authentication, Authentication)


@responses.activate
def test_raises(client, error):
    responses.add(responses.GET, URL, status=400, json=error)

    with pytest.raises(IGApiException):
        client.long_lived_token(fake.uuid4())
