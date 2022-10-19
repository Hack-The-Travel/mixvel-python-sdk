# -*- coding: utf-8 -*-
import datetime

from .utils import load_response
from mixvel.parsers import is_cancel_success, parse_order_view
from mixvel.models import MixOrder

import pytest


class TestParsers:
    @pytest.mark.parametrize("resp_path", [
        "responses/order/cancel_success.xml",
    ])
    def test_is_cancel_success(self, resp_path):
        resp = load_response(resp_path)
        assert is_cancel_success(resp)

    def test_parse_order_view(self):
        order = MixOrder(
            "00999-210624-MEE0458",  # mix order id
            "04G82X",  # booking id
            datetime.datetime(2021, 9, 23, 0, 40, 0)  # ttl
        )
        resp = load_response("responses/order/view.xml")
        got = parse_order_view(resp)

        assert got.mix_order_id == order.mix_order_id
        assert got.booking_id == order.booking_id
        assert got.time_limit == order.time_limit
