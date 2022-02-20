import urllib

import requests

from schemas import Authentication


class InstagramBasicDisplayClient:
    API_ENDPOINT = "https://api.instagram.com"
    GRAPH_ENDPOINT = "https://graph.instagram.com"

    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        scope="user_profile,user_media",
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.client_secret = client_secret

    def authorize(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "response_type": "code",
        }

        url = (
            f"{self.API_ENDPOINT}/oauth/authorize?"
            f"{urllib.parse.urlencode(params)}"
        )

        return url

    def exchange(self, code):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        url = f"{self.API_ENDPOINT}/oauth/access_token"
        resp = requests.post(url, data=data)

        return Authentication(**resp.json(), expires_in=3600)

    def long_lived_token(self, access_token):
        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.client_secret,
            "access_token": access_token,
        }

        url = f"{self.GRAPH_ENDPOINT}/access_token"
        resp = requests.get(url, params=params)

        return Authentication(**resp.json())
