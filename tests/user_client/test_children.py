import re

import responses
from faker import Faker
from responses import matchers

fake = Faker()


@responses.activate
def test_call(user_client, children):
    id_ = fake.pyint()
    params = {
        "fields": user_client._fields_children,
        "access_token": user_client.authentication.access_token,
    }
    responses.add(
        responses.GET,
        re.compile(r".+\d+/children"),
        json={"data": [children.dict()]},
        match=[matchers.query_param_matcher(params)],
    )

    user_client.children(id_)

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_response(user_client, children):
    id_ = fake.pyint()
    responses.add(
        responses.GET,
        re.compile(r".+\d+/children"),
        json={"data": [children.dict()]},
    )

    childrens = user_client.children(id_)

    assert childrens == [children]
