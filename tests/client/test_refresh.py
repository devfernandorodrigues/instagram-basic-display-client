import pytest
import requests
import responses
from faker import Faker
from responses import matchers

from instabd.schemas import Authentication

fake = Faker()

URL = "https://graph.instagram.com/refresh_access_token"


@responses.activate
def test_call(client):
    access_token = fake.uuid4()
    params = {
        "grant_type": "ig_refresh_token",
        "access_token": access_token,
    }
    responses.add(
        responses.GET,
        URL,
        json={"access_token": access_token},
        match=[matchers.query_param_matcher(params)],
    )

    client.refresh(access_token)

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_response(client):
    access_token = fake.uuid4()
    responses.add(
        responses.GET,
        URL,
        json={"access_token": access_token, "expires_in": 5183944},
    )

    authentication = client.refresh(fake.uuid4())

    assert authentication.access_token == access_token
    assert authentication.expires_at is not None


@responses.activate
def test_instance(client):
    responses.add(
        responses.GET,
        URL,
        json={"access_token": fake.uuid4()},
    )

    authentication = client.refresh(fake.uuid4())

    assert isinstance(authentication, Authentication)


@responses.activate
def test_raises(client):
    responses.add(
        responses.GET,
        URL,
        status=400,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        client.refresh(fake.uuid4())
