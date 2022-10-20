# -*- coding: utf-8 -*-
import datetime

from .utils import load_response
from mixvel.parsers import is_cancel_success, parse_order_view
from mixvel.models import (
    Amount, Booking, MixOrder, Order
)

import pytest


class TestParsers:
    @pytest.mark.parametrize("resp_path", [
        "responses/order/cancel_success.xml",
    ])
    def test_is_cancel_success(self, resp_path):
        resp = load_response(resp_path)
        assert is_cancel_success(resp)

    def test_parse_order_view(self):
        mix_order = MixOrder(
            "00999-210624-MEE0458",  # mix order id
            [
                Order(
                    "00999-210624-OEE0459",
                    [
                        Booking("04G82X"),
                    ],
                    datetime.datetime(2021, 9, 23, 0, 40, 0),  # tttl
                    Amount(653800, "RUB"),  # order total amount
                ),
            ],
            Amount(653800, "RUB")  # total amount
        )
        resp = load_response("responses/order/view.xml")
        got = parse_order_view(resp)

        assert got.mix_order_id == mix_order.mix_order_id
        assert got.total_amount.amount == mix_order.total_amount.amount
        assert got.total_amount.cur_code == mix_order.total_amount.cur_code

        # orders
        assert len(got.orders) == len(mix_order.orders)
        for i in range(len(got.orders)):
            assert got.orders[i].order_id == mix_order.orders[i].order_id
            assert got.orders[i].deposit_timelimit == mix_order.orders[i].deposit_timelimit
            assert got.orders[i].total_amount.amount == mix_order.orders[i].total_amount.amount
            assert got.orders[i].total_amount.cur_code == mix_order.orders[i].total_amount.cur_code

            # booking_refs
            assert len(got.orders[i].booking_refs) == len(mix_order.orders[i].booking_refs)
            for j in range(len(got.orders[i].booking_refs)):
                assert got.orders[i].booking_refs[j].booking_id \
                    == mix_order.orders[i].booking_refs[j].booking_id
