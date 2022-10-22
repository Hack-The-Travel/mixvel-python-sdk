# -*- coding: utf-8 -*-
from .utils import parse_xml
from mixvel.utils import lxml_remove_namespaces

import pytest


class TestUtils:
    @pytest.mark.parametrize("resp_path", [
        "responses/accounts/login_error.xml",
    ])
    def test_lxml_remove_namespace(self, resp_path):
        resp = parse_xml(resp_path)
        assert resp.find(".//AuthResponse") is None
        lxml_remove_namespaces(resp)
        assert resp.find(".//AuthResponse") is not None
