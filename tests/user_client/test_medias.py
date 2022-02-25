import re

import responses

from schemas import MediaType

URL = "https://graph.instagram.com/me/media"


@responses.activate
def test_response(user_client, media):
    data = {"data": [media.dict()]}
    responses.add(responses.GET, URL, json=data)

    medias = user_client.medias()

    assert medias == [media]


@responses.activate
def test_params(user_client, media):
    data = {"data": [media.dict()]}
    params = {
        "access_token": user_client.authentication.access_token,
        "fields": user_client._fields,
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
        json={"data": [media.dict()]},
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
        json={"data": [media.dict()]},
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
        json={"data": [media.dict()]},
        status=200,
    )

    user_client.medias()

    assert len(responses.calls) == 1
