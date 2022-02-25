import urllib
from functools import cached_property

import requests

from schemas import Authentication
from schemas import Children
from schemas import Media
from schemas import MediaType
from schemas import User


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

    def request(self, method, url, *args, **kwargs):
        resp = requests.request(method, url, *args, **kwargs)
        resp.raise_for_status()
        return resp

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
        resp = self.request("post", url, data=data)

        return Authentication(**resp.json(), expires_in=3600)

    def long_lived_token(self, access_token):
        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.client_secret,
            "access_token": access_token,
        }

        url = f"{self.GRAPH_ENDPOINT}/access_token"
        resp = self.request("get", url, params=params)

        return Authentication(**resp.json())

    def refresh(self, access_token):
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": access_token,
        }

        url = f"{self.GRAPH_ENDPOINT}/refresh_access_token"
        resp = self.request("get", url, params=params)

        return Authentication(**resp.json())

    def exchange_long(self, code):
        authentication = self.exchange(code)
        long_authentication = self.long_lived_token(
            authentication.access_token,
        )
        return long_authentication

    def to_user_client_from_code(self, code, long=False):
        if long:
            authentication = self.exchange_long(code)
        else:
            authentication = self.exchange(code)

        return UserClient(
            authentication=authentication,
        )


class UserClient:
    ENDPOINT = "https://graph.instagram.com"

    def __init__(self, authentication):
        self.authentication = authentication
        self._fields = (
            "id,caption,media_type,media_url,permalink,"
            "thumbnail_url,timestamp,username"
        )
        self._fields_children = (
            "id,media_type,media_url,permalink,"
            "thumbnail_url,timestamp,username"
        )

    @cached_property
    def user(self):
        params = {
            "fields": "id,username",
            "access_token": self.authentication.access_token,
        }

        url = f"{self.ENDPOINT}/me"
        resp = requests.get(url, params=params)

        return User(**resp.json())

    def medias(self):
        params = {
            "access_token": self.authentication.access_token,
            "fields": self._fields,
        }

        url = f"{self.ENDPOINT}/me/media"

        resp = requests.get(url, params=params)
        data = resp.json()["data"]

        medias = []
        for d in data:
            media = Media(**d)
            if media.media_type == MediaType.carousel_album.value:
                media.children = self.children(media.id)
            medias.append(media)

        return medias

    def children(self, id_):
        params = {
            "fields": self._fields_children,
            "access_token": self.authentication.access_token,
        }

        url = f"{self.ENDPOINT}/{id_}/children"

        resp = requests.get(url, params=params)
        data = resp.json()["data"]

        return [Children(**media) for media in data]

    @staticmethod
    def from_access_token(access_token):
        return UserClient(
            authentication=Authentication(
                access_token=access_token,
            )
        )
