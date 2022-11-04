# -*- coding: utf-8 -*-
import datetime

from .utils import load_response
from mixvel._parsers import (
    is_cancel_success, parse_order_view,
)
from mixvel._parsers import (
    parse_amount, parse_fare_component, parse_fare_detail, parse_price,
    parse_tax,
)  # type parsers
from mixvel.models import (
    Amount, Booking, FareComponent, FareDetail,
    MixOrder, Order, Price, Tax,
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


class TestTypeParsers:
    @pytest.mark.parametrize("model_path,want", [
        (
            "models/amount_1.xml",
            Amount(653800, "RUB"),
        ),
        (
            "models/amount_2.xml",
            Amount(326900, "RUB"),
        ),
    ])
    def test_parse_amount(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False).getroot()
        got = parse_amount(elm)
        assert got.amount == want.amount
        assert got.cur_code == want.cur_code

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/fare_component.xml",
            FareComponent("RPROWRF", Price([], Amount(326900, "RUB"))),
        ),
    ])
    def test_parse_fare_componentl(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_fare_component(elm)
        assert got.fare_basis_code == want.fare_basis_code
        assert isinstance(got.price, Price)

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/fare_detail.xml",
            FareDetail([], "Pax-1"),
        ),
    ])
    def test_parse_fare_detail(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_fare_detail(elm)
        assert isinstance(got.fare_components[0], FareComponent)
        assert got.pax_ref_id == want.pax_ref_id

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/price.xml",
            Price([], Amount(326900, "RUB")),
        ),
    ])
    def test_parse_price(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_price(elm)
        assert got.total_amount.amount == want.total_amount.amount

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/tax__zero_amount.xml",
            Tax(Amount(0, None), "ZZ"),
        ),
    ])
    def test_parse_tax(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_tax(elm)
        assert got.amount.amount == want.amount.amount
        assert got.amount.cur_code == want.amount.cur_code
        assert got.tax_code == want.tax_code
