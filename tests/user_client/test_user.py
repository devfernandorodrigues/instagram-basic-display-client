import pytest
import responses
from faker import Faker
from responses import matchers

from instabd.exceptions import IGApiException
from instabd.schemas import User


fake = Faker()

URL = "https://graph.instagram.com/me"


@responses.activate
def test_call(user_client):
    params = {
        "fields": "id,account_type,username,media_count",
        "access_token": user_client.authentication.access_token,
    }
    responses.add(
        responses.GET,
        URL,
        json={
            "id": fake.uuid4(),
            "username": fake.user_name(),
            "media_count": fake.pyint(),
            "account_type": "BUSINESS",
        },
        match=[matchers.query_param_matcher(params)],
    )

    user_client.user

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_response(user_client):
    json_data = {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "media_count": fake.pyint(),
        "account_type": "BUSINESS",
    }
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert user.id == json_data["id"]
    assert user.username == json_data["username"]
    assert user.media_count == json_data["media_count"]
    assert user.account_type == json_data["account_type"]


@responses.activate
def test_istance(user_client):
    json_data = {
        "id": fake.uuid4(),
        "username": fake.user_name(),
        "media_count": fake.pyint(),
        "account_type": "BUSINESS",
    }
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert isinstance(user, User)


@responses.activate
def test_raises(user_client, error):
    responses.add(responses.GET, URL, status=400, json=error)

    with pytest.raises(IGApiException):
        user_client.user
