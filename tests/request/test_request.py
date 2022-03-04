import re

import pytest
import requests
import responses

from instabd.exceptions import IGApiBadRequestException
from instabd.exceptions import IGApiCodedException
from instabd.exceptions import IGApiException
from instabd.exceptions import IGApiForbiddenException
from instabd.exceptions import IGApiUnauthorizedException


@responses.activate
def test_raises_on_400(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "IGApiException",
                "code": 100,
                "error_subcode": 33,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=400,
    )

    with pytest.raises(IGApiException):
        req("get", faker.url())


@responses.activate
def test_raises_on_400_and_code_100(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "IGApiBadRequestException",
                "code": 100,
                "error_subcode": None,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=400,
    )

    with pytest.raises(IGApiBadRequestException):
        req("get", faker.url())


@responses.activate
def test_raises_on_400_and_code_190(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "IGApiException",
                "code": 190,
                "error_subcode": None,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=400,
    )

    with pytest.raises(IGApiUnauthorizedException):
        req("get", faker.url())


@responses.activate
def test_raises_on_403_and_code_4(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "CodedException",
                "code": 4,
                "error_subcode": None,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=403,
    )

    with pytest.raises(IGApiCodedException):
        req("get", faker.url())


@responses.activate
def test_raises_on_403_and_code_10(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "IGApiForbiddenException",
                "code": 10,
                "error_subcode": None,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=403,
    )

    with pytest.raises(IGApiForbiddenException):
        req("get", faker.url())


@responses.activate
def test_raises_on_403_and_code_200(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={
            "error": {
                "message": "...",
                "type": "IGApiForbiddenException",
                "code": 200,
                "error_subcode": None,
                "fbtrace_id": "At9_KmV0NHMck-Lmr_FuEki",
            }
        },
        status=403,
    )

    with pytest.raises(IGApiForbiddenException):
        req("get", faker.url())


@responses.activate
def test_raises_for_status(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={},
        status=405,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        req("get", faker.url())


@responses.activate
def test_response(req, faker):
    responses.add(
        responses.GET,
        re.compile(".*"),
        json={},
        status=200,
    )

    resp = req("get", faker.url())

    assert isinstance(resp, requests.Response)
