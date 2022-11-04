# -*- coding: utf-8 -*-
import datetime

from .utils import load_response
from mixvel._parsers import (
    is_cancel_success, parse_order_view,
)
from mixvel._parsers import (
    parse_amount, parse_booking, parse_fare_component, parse_fare_detail,
    parse_mix_order, parse_order_item, parse_order, parse_price,
    parse_tax,
)
from mixvel.models import (
    OrderViewResponse,
)
from mixvel.models import (
    Amount, Booking, FareComponent, FareDetail,
    MixOrder, Order, OrderItem, Price,
    Tax,
)

import pytest


class TestParsers:
    @pytest.mark.parametrize("resp_path", [
        "responses/order/cancel_success.xml",
    ])
    def test_is_cancel_success(self, resp_path):
        resp = load_response(resp_path)
        assert is_cancel_success(resp)

    @pytest.mark.parametrize("resp_path", [
        "responses/order/view.xml",
    ])
    def test_parse_order_view(self, resp_path):
        resp = load_response(resp_path)
        got = parse_order_view(resp)
        assert isinstance(got, OrderViewResponse)
        assert isinstance(got.mix_order, MixOrder)

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
            "models/booking.xml",
            Booking("04G82X"),
        ),
    ])
    def test_parse_booking(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False).getroot()
        got = parse_booking(elm)
        assert got.booking_id == want.booking_id

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
            "models/mix_order.xml",
            MixOrder("00999-210624-MEE0458", [], Amount(653800, "RUB")),
        ),
    ])
    def test_parse_mix_order(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False).getroot()
        got = parse_mix_order(elm)
        assert got.mix_order_id == want.mix_order_id
        assert isinstance(got.orders[0], Order)
        assert isinstance(got.total_amount, Amount)

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/order.xml",
            Order(
                "00999-210624-OEE0459",
                [],
                datetime.datetime(2021, 9, 23, 0, 40, 0),
                Price([], Amount(653800, "RUB")),
            ),
        ),
    ])
    def test_parse_order(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_order(elm)
        assert got.order_id == want.order_id
        assert isinstance(got.booking_refs[0], Booking)
        assert got.deposit_timelimit == want.deposit_timelimit
        assert isinstance(got.total_price, Price)

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/order_item.xml",
            OrderItem(
                "fa21bac3-6a8c-4066-8477-148bc5f63a31",
                [],
                Price([], Amount(653800, "RUB"))
            ),
        ),
    ])
    def test_parse_order_item(self, model_path, want):
        elm = load_response(model_path, clean_appdata=False)
        got = parse_order_item(elm)
        assert got.order_item_id == want.order_item_id
        assert isinstance(got.fare_details[0], FareDetail)
        assert isinstance(got.price, Price)

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
