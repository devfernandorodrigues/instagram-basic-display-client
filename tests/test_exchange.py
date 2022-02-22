from unittest.mock import Mock

import pytest
import requests
import responses
from faker import Faker

from schemas import Authentication

fake = Faker()

URL = "https://api.instagram.com/oauth/access_token"


def test_call_mock(client, mocker):
    mock = mocker.patch(
        "client.InstagramBasicDisplayClient.request",
        return_value=Mock(
            status_code=200,
            json=lambda: {"access_token": fake.uuid4()},
        ),
    )
    code = fake.uuid4()
    data = {
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": client.redirect_uri,
        "code": code,
    }

    client.exchange(code)

    mock.assert_called_once_with("post", URL, data=data)


@responses.activate
def test_response(client):
    access_token = fake.uuid4()
    code = fake.uuid4()
    responses.add(
        responses.POST,
        URL,
        json={"access_token": access_token},
    )

    authentication = client.exchange(code)

    assert authentication.access_token == access_token


@responses.activate
def test_instance(client):
    code = fake.uuid4()
    responses.add(
        responses.POST,
        URL,
        json={"access_token": fake.uuid4()},
    )

    authentication = client.exchange(code)

    assert isinstance(authentication, Authentication)


@responses.activate
def test_schema(client, mocker):
    code = fake.uuid4()
    json_data = {"access_token": fake.uuid4()}
    responses.add(
        responses.POST,
        URL,
        json=json_data,
    )
    mock = mocker.patch("client.Authentication")

    client.exchange(code)

    mock.assert_called_once_with(**json_data, expires_in=3600)


@responses.activate
def test_raises(client, mocker):
    code = fake.uuid4()
    responses.add(responses.POST, URL, status=400)

    with pytest.raises(requests.exceptions.HTTPError):
        client.exchange(code)
