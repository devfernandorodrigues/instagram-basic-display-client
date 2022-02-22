from unittest.mock import Mock

import responses
from faker import Faker

from client import UserClient
from schemas import Authentication
from schemas import User


fake = Faker()

URL = "https://graph.instagram.com/me"


def test_call_mock(mocker):
    access_token = fake.uuid4()
    params = {"fields": "id,username", "access_token": access_token}
    user_client = UserClient(
        authentication=Authentication(
            access_token=access_token,
        )
    )
    mock = mocker.patch(
        "requests.get",
        return_value=Mock(
            status_code=200,
            json=lambda: {"id": fake.uuid4(), "username": fake.user_name()},
        ),
    )

    user_client.user

    mock.assert_called_once_with(URL, params=params)


@responses.activate
def test_response():
    access_token = fake.uuid4()
    json_data = {"id": fake.uuid4(), "username": fake.user_name()}
    user_client = UserClient(
        authentication=Authentication(
            access_token=access_token,
        )
    )
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert user.id == json_data["id"]
    assert user.username == json_data["username"]


@responses.activate
def test_istance():
    access_token = fake.uuid4()
    json_data = {"id": fake.uuid4(), "username": fake.user_name()}
    user_client = UserClient(
        authentication=Authentication(
            access_token=access_token,
        )
    )
    responses.add(responses.GET, URL, json=json_data)

    user = user_client.user

    assert isinstance(user, User)


@responses.activate
def test_schema(mocker):
    access_token = fake.uuid4()
    json_data = {"id": fake.uuid4(), "username": fake.user_name()}
    user_client = UserClient(
        authentication=Authentication(
            access_token=access_token,
        )
    )
    responses.add(responses.GET, URL, json=json_data)
    mock = mocker.patch("client.User")

    user_client.user

    mock.assert_called_once_with(**json_data)
