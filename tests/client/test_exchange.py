import pytest
import requests
import responses
from faker import Faker
from responses import matchers

from instabd.schemas import Authentication

fake = Faker()

URL = "https://api.instagram.com/oauth/access_token"


@responses.activate
def test_call(client):
    code = fake.uuid4()
    data = {
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "grant_type": "authorization_code",
        "redirect_uri": client.redirect_uri,
        "code": code,
    }
    responses.add(
        responses.POST,
        URL,
        json={"access_token": fake.uuid4()},
        match=[matchers.urlencoded_params_matcher(data)],
    )

    client.exchange(code)

    assert responses.calls[0].response.status_code == 200


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
def test_raises(client):
    code = fake.uuid4()
    responses.add(responses.POST, URL, status=400)

    with pytest.raises(requests.exceptions.HTTPError):
        client.exchange(code)
