import re

import responses


@responses.activate
def test_call(client, faker):
    responses.add(
        responses.POST,
        re.compile(r".+/oauth\/access_token"),
        json={"access_token": faker.uuid4()},
    )
    responses.add(
        responses.GET,
        re.compile(r".*/access_token.*"),
        json={"access_token": faker.uuid4()},
    )

    client.exchange_long(faker.uuid4())

    assert len(responses.calls) == 2


@responses.activate
def test_response(client, faker):
    access_token = faker.uuid4()
    responses.add(
        responses.POST,
        re.compile(r".+/oauth/access_token"),
        json={"access_token": faker.uuid4()},
    )
    responses.add(
        responses.GET,
        re.compile(r".*/access_token.*"),
        json={"access_token": access_token},
    )

    long_authentication = client.exchange_long(faker.uuid4())

    assert long_authentication.access_token == access_token
