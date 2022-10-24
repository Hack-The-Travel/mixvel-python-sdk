# -*- coding: utf-8 -*-
import datetime

from .utils import parse_xml, parse_xml_response
from mixvel._parsers import (
    is_cancel_success, parse_order_view,
)
from mixvel._parsers import (
    parse_amount, parse_booking, parse_fare_component, parse_fare_detail,
    parse_mix_order, parse_offer, parse_offer_item, parse_order_item,
    parse_order, parse_price, parse_rbd_avail, parse_service,
    parse_service_offer_associations, parse_tax,
)
from mixvel.models import (
    OrderViewResponse,
)
from mixvel.models import (
    Amount, Booking, FareComponent, FareDetail,
    MixOrder, Offer, OfferItem, Order,
    OrderItem, Price, RbdAvail, Service,
    ServiceOfferAssociations, Tax,
)

import pytest


class TestParsers:
    @pytest.mark.parametrize("resp_path", [
        "responses/order/cancel_success.xml",
    ])
    def test_is_cancel_success(self, resp_path):
        resp = parse_xml_response(resp_path)
        assert is_cancel_success(resp)

    @pytest.mark.parametrize("resp_path", [
        "responses/order/view.xml",
    ])
    def test_parse_order_view(self, resp_path):
        resp = parse_xml_response(resp_path)
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
        elm = parse_xml(model_path).getroot()
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
        elm = parse_xml(model_path).getroot()
        got = parse_booking(elm)
        assert got.booking_id == want.booking_id

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/fare_component.xml",
            FareComponent("RPROWRF", Price([], Amount(326900, "RUB"))),
        ),
    ])
    def test_parse_fare_componentl(self, model_path, want):
        elm = parse_xml(model_path)
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
        elm = parse_xml(model_path)
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
        elm = parse_xml(model_path).getroot()
        got = parse_mix_order(elm)
        assert got.mix_order_id == want.mix_order_id
        assert isinstance(got.orders[0], Order)
        assert isinstance(got.total_amount, Amount)

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/offer.xml",
            Offer(
                "63ac5143-927c-4b21-8ba5-41061fa5b2c3",  # offer_id
                [],  # offer_items
                "TCH"  # owner_code
            ),
        ),
    ])
    def test_parse_offer(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_offer(elm)
        assert got.offer_id == want.offer_id
        assert isinstance(got.offer_items[0], OfferItem)
        assert got.owner_code == want.owner_code

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/offer_item.xml",
            OfferItem(
                "ca280e53-1dd1-4d7b-9b57-d1a45b364f29",  # offer_item_id
                Price([], Amount(332400, "RUB")),  # price
                [],  # services
                fare_details=[]  # fare_details
            ),
        ),
    ])
    def test_parse_offer_item(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_offer_item(elm)
        assert got.offer_item_id == want.offer_item_id
        assert isinstance(got.price, Price)
        assert isinstance(got.services[0], Service)
        assert isinstance(got.fare_details[0], FareDetail)

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/order.xml",
            Order(
                "00999-210624-OEE0459",
                [],  # order_items
                [],  # booking_refs
                datetime.datetime(2021, 9, 23, 0, 40, 0),
                Price([], Amount(653800, "RUB")),
            ),
        ),
    ])
    def test_parse_order(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_order(elm)
        assert got.order_id == want.order_id
        assert isinstance(got.order_items[0], OrderItem)
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
        elm = parse_xml(model_path)
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
        elm = parse_xml(model_path)
        got = parse_price(elm)
        assert got.total_amount.amount == want.total_amount.amount

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/rbd_avail.xml",
            RbdAvail("A", availability=9),
        ),
    ])
    def test_rbd_avail(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_rbd_avail(elm)
        assert got.rbd_code == want.rbd_code
        assert got.availability == want.availability

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/service.xml",
            Service(
                "fd45bc97-0e26-48bd-aa2a-7c49672e604a",  # service_id
                ["Pax-1", "Pax-2"],  # pax_ref_ids
                ServiceOfferAssociations(),  # service_associations
                validating_party_ref_id="7036ae6a-a67e-4986-a6f6-60465a7beadc"
            ),
        ),
    ])
    def test_parse_service(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_service(elm)
        assert got.service_id == want.service_id
        assert len(got.pax_ref_ids) == len(want.pax_ref_ids)
        for i in range(len(want.pax_ref_ids)):
            got.pax_ref_ids[i] == want.pax_ref_ids[i]
        assert isinstance(got.service_associations, ServiceOfferAssociations)
        assert got.validating_party_ref_id == want.validating_party_ref_id

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/service_offer_associations.xml",
            ServiceOfferAssociations(pax_journey_ref_ids=[
                "94be4cd4-c9b0-42d2-be5b-9775830c668f",
                "54728d42-73b5-42e9-8fb5-4b7982e294d0",
            ]),
        ),
    ])
    def test_parse_service_offer_associations(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_service_offer_associations(elm)
        assert len(want.pax_journey_ref_ids) == len(got.pax_journey_ref_ids)
        for i in range(len(want.pax_journey_ref_ids)):
            got.pax_journey_ref_ids[i] == want.pax_journey_ref_ids[i]

    @pytest.mark.parametrize("model_path,want", [
        (
            "models/tax__zero_amount.xml",
            Tax(Amount(0, None), "ZZ"),
        ),
    ])
    def test_parse_tax(self, model_path, want):
        elm = parse_xml(model_path)
        got = parse_tax(elm)
        assert got.amount.amount == want.amount.amount
        assert got.amount.cur_code == want.amount.cur_code
        assert got.tax_code == want.tax_code
