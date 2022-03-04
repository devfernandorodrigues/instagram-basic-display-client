import requests

from instabd.exceptions import IGApiBadRequestException
from instabd.exceptions import IGApiCodedException
from instabd.exceptions import IGApiException
from instabd.exceptions import IGApiForbiddenException
from instabd.exceptions import IGApiUnauthorizedException
from instabd.schemas import Error


def handle_hook(response, *args, **kwargs):
    if response.status_code == 400:
        error = Error(**response.json()["error"])

        if error.code == 100 and not error.error_subcode:
            raise IGApiBadRequestException(error.dict())

        if error.code == 100 and error.error_subcode == 33:
            raise IGApiException(error.dict())

        if error.code == 190:
            raise IGApiUnauthorizedException(error.dict())

    if response.status_code == 403:
        error = Error(**response.json()["error"])

        if error.code == 4:
            raise IGApiCodedException(error.dict())

        if error.code == 10 or error.code == 200:
            raise IGApiForbiddenException(error.dict())


def request(method, url, *args, **kwargs):
    resp = requests.request(
        method, url, *args, hooks={"response": handle_hook}, **kwargs
    )
    resp.raise_for_status()
    return resp
