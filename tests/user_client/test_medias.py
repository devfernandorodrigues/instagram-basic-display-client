import responses

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
