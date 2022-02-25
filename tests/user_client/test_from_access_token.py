from client import UserClient


def test_from_access_token(faker):
    access_token = faker.uuid4()

    user_client = UserClient.from_access_token(access_token)

    assert user_client.authentication.access_token == access_token
