from unittest.mock import Mock

import responses
from faker import Faker

from schemas import Authentication

fake = Faker()

URL = "https://graph.instagram.com/access_token"


def test_call_mock(client, mocker):
    mock = mocker.patch(
        "requests.get",
        return_value=Mock(
            status_code=200,
            json=lambda: {"access_token": fake.uuid4()},
        ),
    )
    access_token = fake.uuid4()
    params = {
        "grant_type": "ig_exchange_token",
        "client_secret": client.client_secret,
        "access_token": access_token,
    }

    client.long_lived_token(access_token)

    mock.assert_called_once_with(URL, params=params)


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
def test_schema(client, mocker):
    json_data = {
        "access_token": fake.uuid4(),
        "expires_in": fake.pyint(),
    }
    responses.add(
        responses.GET,
        URL,
        json=json_data,
    )
    mock = mocker.patch("client.Authentication")

    client.long_lived_token(fake.uuid4())

    mock.assert_called_once_with(**json_data)
