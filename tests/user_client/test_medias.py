import re
from datetime import datetime

import responses

from instabd.schemas import MediaType

URL = "https://graph.instagram.com/me/media"


@responses.activate
def test_response(user_client, media):
    data = {"data": [media.dict()], "paging": {}}
    responses.add(responses.GET, URL, json=data)

    medias = user_client.medias()

    assert medias == [media]


@responses.activate
def test_params(user_client, media):
    data = {"data": [media.dict()], "paging": {}}
    params = {
        "access_token": user_client.authentication.access_token,
        "fields": user_client._fields,
        "limit": "10",
    }
    responses.add(responses.GET, URL, json=data, status=200)

    user_client.medias()

    assert responses.calls[0].request.params == params


@responses.activate
def test_children(user_client, media, children):
    media.media_type = MediaType.carousel_album.value
    responses.add(
        responses.GET,
        URL,
        json={"data": [media.dict()], "paging": {}},
        status=200,
    )
    responses.add(
        responses.GET,
        re.compile(r".+children"),
        json={"data": [children.dict()]},
    )

    medias = user_client.medias()

    assert len(responses.calls) == 2
    assert medias[0].children[0] == children


@responses.activate
def test_image_media_type(user_client, media):
    media.media_type = MediaType.image.value
    responses.add(
        responses.GET,
        URL,
        json={"data": [media.dict()], "paging": {}},
        status=200,
    )

    user_client.medias()

    assert len(responses.calls) == 1


@responses.activate
def test_video_media_type(user_client, media):
    media.media_type = MediaType.video.value
    responses.add(
        responses.GET,
        URL,
        json={"data": [media.dict()], "paging": {}},
        status=200,
    )

    user_client.medias()

    assert len(responses.calls) == 1


@responses.activate
def test_next(user_client, media):
    responses.add(
        responses.GET,
        URL,
        json={
            "data": [media.dict() for i in range(0, 10)],
            "paging": {
                "next": f"{URL}/next",
            },
        },
    )
    responses.add(
        responses.GET,
        f"{URL}/next",
        json={
            "data": [media.dict() for i in range(0, 10)],
            "paging": {
                "next": URL,
            },
        },
    )

    medias = user_client.medias(
        limit=20,
    )

    assert len(medias) == 20
    assert len(responses.calls) == 2
    assert "/next" not in responses.calls[0].request.url
    assert "/next" in responses.calls[1].request.url


@responses.activate
def test_limit(user_client, media):
    responses.add(
        responses.GET,
        URL,
        json={
            "data": [media.dict() for i in range(0, 10)],
            "paging": {
                "next": f"{URL}/next",
            },
        },
    )

    medias = user_client.medias(
        limit=10,
    )

    assert len(medias) == 10
    assert len(responses.calls) == 1


@responses.activate
def test_grab_all(user_client, media):
    for i in range(0, 5):
        responses.add(
            responses.GET,
            re.compile(rf"{URL}.+"),
            json={
                "data": [media.dict() for i in range(0, 10)],
                "paging": {
                    "next": f"{URL}/next" if i != 4 else None,
                },
            },
        )

    medias = user_client.medias(grab_all=True)

    assert len(responses.calls) == 5
    assert len(medias) == 50


@responses.activate
def test_limit_length(user_client, media):
    for i in range(0, 5):
        responses.add(
            responses.GET,
            re.compile(rf"{URL}.+"),
            json={
                "data": [media.dict() for i in range(0, 10)],
                "paging": {
                    "next": f"{URL}/next" if i != 4 else None,
                },
            },
        )

    medias = user_client.medias(limit=25)

    assert len(medias) == 25


@responses.activate
def test_since_param(user_client, media):
    data = {"data": [media.dict()], "paging": {}}
    params = {
        "access_token": user_client.authentication.access_token,
        "fields": user_client._fields,
        "limit": "10",
        "since": str(datetime.now().timestamp()),
    }
    responses.add(responses.GET, URL, json=data, status=200)

    user_client.medias(since=params["since"])

    assert responses.calls[0].request.params == params


@responses.activate
def test_until_param(user_client, media):
    data = {"data": [media.dict()], "paging": {}}
    params = {
        "access_token": user_client.authentication.access_token,
        "fields": user_client._fields,
        "limit": "10",
        "until": str(datetime.now().timestamp()),
    }
    responses.add(responses.GET, URL, json=data, status=200)

    user_client.medias(until=params["until"])

    assert responses.calls[0].request.params == params


@responses.activate
def test_wihtout_paging(user_client):
    responses.add(responses.GET, URL, json={"data": []}, status=200)

    user_client.medias()

    assert responses.calls[0].response.status_code == 200
