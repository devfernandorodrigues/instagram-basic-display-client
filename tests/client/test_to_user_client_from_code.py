import re

import responses

from user_client import UserClient


@responses.activate
def test_user_client(client, faker):
    responses.add(
        responses.POST,
        re.compile(r".+access_token"),
        json={"access_token": faker.uuid4()},
    )

    client.to_user_client_from_code(faker.uuid4())

    assert len(responses.calls) == 1


@responses.activate
def test_response(client, faker):
    responses.add(
        responses.POST,
        re.compile(r".+access_token"),
        json={"access_token": faker.uuid4()},
    )

    user_client = client.to_user_client_from_code(faker.uuid4())

    assert isinstance(user_client, UserClient)


@responses.activate
def test_long(client, faker):
    access_token = faker.uuid4()
    responses.add(
        responses.POST,
        re.compile(r".+access_token"),
        json={"access_token": faker.uuid4()},
    )
    responses.add(
        responses.GET,
        re.compile(r".+access_token.+"),
        json={"access_token": access_token},
    )

    user_client = client.to_user_client_from_code(faker.uuid4(), long=True)

    assert user_client.authentication.access_token == access_token
