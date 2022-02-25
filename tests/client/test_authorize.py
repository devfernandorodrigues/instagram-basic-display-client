import urllib

from faker import Faker

from instabd.client import InstabdClient

fake = Faker()

AUTHORIZE_URL = "https://api.instagram.com/oauth/authorize"


def test_url():
    client_id = fake.uuid4()
    client_secret = fake.uuid4()
    redirect_uri = fake.url()
    scope = "user_profile,user_media"
    client = InstabdClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
    }
    expected_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    url = client.authorize()

    assert url == expected_url


def test_scope():
    client_id = fake.uuid4()
    client_secret = fake.uuid4()
    redirect_uri = fake.url()
    scope = "user_profile"
    client = InstabdClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
    }
    expected_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    url = client.authorize()

    assert url == expected_url
