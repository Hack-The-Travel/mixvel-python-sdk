# -*- coding: utf-8 -*-
from .utils import load_response
from mixvel.parsers import is_cancel_success

import pytest

class TestParsers:
    @pytest.mark.parametrize('resp_path', [
        'responses/order/cancel_success.xml',
    ])
    def test_lxml_remove_namespace(self, resp_path):
        resp = load_response(resp_path)
        assert is_cancel_success(resp)
