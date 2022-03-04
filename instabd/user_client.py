from functools import cached_property

import requests

from .schemas import Authentication
from .schemas import Children
from .schemas import Media
from .schemas import MediaType
from .schemas import User


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
            "fields": "id,account_type,username,media_count",
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
