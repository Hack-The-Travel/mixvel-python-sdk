# -*- coding: utf-8 -*-
import os
import pytest
import logging
from mixvel.client import (
    TEST_GATEWAY,
    Client,
)

# configure logging to output to console during tests
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_auth():
    login = os.getenv("MIXVEL_LOGIN")
    password = os.getenv("MIXVEL_PASSWORD")
    structure_unit_id = os.getenv("MIXVEL_STRUCTURE_ID")

    if not all([login, password, structure_unit_id]):
        pytest.skip(
            "Skipping test: MIXVEL_LOGIN, MIXVEL_PASSWORD, or MIXVEL_STRUCTURE_ID not set in environment"
        )

    client = Client(login, password, structure_unit_id, gateway=TEST_GATEWAY)
    token = client.auth()
    assert isinstance(token, str)
    assert len(token) > 0
    assert client.token == token
