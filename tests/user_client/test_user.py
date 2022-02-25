import responses
from faker import Faker
from responses import matchers

from instabd.schemas import User


fake = Faker()

URL = "https://graph.instagram.com/me"


@responses.activate
def test_call_mock(user_client):
    params = {
        "fields": "id,username",
        "access_token": user_client.authentication.access_token,
    }
    responses.add(
        responses.GET,
        URL,
        json={"id": fake.uuid4(), "username": fake.user_name()},
        match=[matchers.query_param_matcher(params)],
    )

    user_client.user

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_response(user_client):
    json_data = {"id": fake.uuid4(), "username": fake.user_name()}
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert user.id == json_data["id"]
    assert user.username == json_data["username"]


@responses.activate
def test_istance(user_client):
    json_data = {"id": fake.uuid4(), "username": fake.user_name()}
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert isinstance(user, User)
