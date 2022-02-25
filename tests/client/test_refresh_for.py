import re

import responses


@responses.activate
def test_refresh_for(client, user_client, faker):
    access_token = faker.uuid4()
    responses.add(
        responses.GET,
        re.compile(r".+refresh_access_token.+"),
        json={"access_token": access_token, "expires_in": faker.pyint()},
    )

    client.refresh_for(user_client)

    assert user_client.authentication.access_token == access_token
    assert user_client.authentication.expires_at is not None
