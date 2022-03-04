from functools import cached_property

from .request import request
from .schemas import Authentication
from .schemas import Children
from .schemas import Media
from .schemas import MediaType
from .schemas import Paging
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
        resp = request("get", url, params=params)

        return User(**resp.json())

    def medias(self, limit=10, grab_all=False, since=None, until=None):
        params = {
            "access_token": self.authentication.access_token,
            "fields": self._fields,
            "limit": limit,
            "since": since,
            "until": until,
        }

        url = f"{self.ENDPOINT}/me/media"
        (data, paging) = self._media_request(url, params)
        medias = self._extract_medias(data)

        if grab_all:
            while paging.next:
                (data, paging) = self._media_request(paging.next, params)
                medias.extend(self._extract_medias(data))
        else:
            while paging.next and len(medias) < limit:
                (data, paging) = self._media_request(paging.next, params)
                medias.extend(self._extract_medias(data))
            if len(medias) > limit:
                medias = medias[:limit]

        return medias

    def _media_request(self, url, params):
        resp = request("get", url, params=params)
        resp_json = resp.json()
        data = resp_json["data"]
        paging_dict = resp_json.get("paging", {})
        paging = Paging(**paging_dict)

        return (data, paging)

    def _extract_medias(self, data):
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

        resp = request("get", url, params=params)
        data = resp.json()["data"]

        return [Children(**media) for media in data]

    @staticmethod
    def from_access_token(access_token):
        return UserClient(
            authentication=Authentication(
                access_token=access_token,
            )
        )
