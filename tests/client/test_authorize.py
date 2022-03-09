import urllib

from faker import Faker

fake = Faker()

AUTHORIZE_URL = "https://api.instagram.com/oauth/authorize"


def test_url(client):
    scope = "user_profile,user_media"
    client.scope = scope
    params = {
        "client_id": client.client_id,
        "redirect_uri": client.redirect_uri,
        "scope": scope,
        "response_type": "code",
    }
    expected_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    url = client.authorize()

    assert url == expected_url


def test_scope(client):
    scope = "user_profile"
    client.scope = scope
    params = {
        "client_id": client.client_id,
        "redirect_uri": client.redirect_uri,
        "scope": scope,
        "response_type": "code",
    }
    expected_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    url = client.authorize()

    assert url == expected_url


def test_state(client, faker):
    state = str(faker.uuid4())
    params = {
        "client_id": client.client_id,
        "redirect_uri": client.redirect_uri,
        "scope": "user_profile,user_media",
        "response_type": "code",
        "state": state,
    }
    expected_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    url = client.authorize(state=state)

    assert url == expected_url
