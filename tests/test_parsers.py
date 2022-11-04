# -*- coding: utf-8 -*-
import datetime

from .utils import load_response
from mixvel._parsers import (
    parse_amount, parse_fare_component, parse_fare_detail, is_cancel_success,
    parse_order_view, parse_price,
)
from mixvel.models import (
    Amount, Booking, FareComponent, FareDetail,
    MixOrder, Order, Price, Tax,
)

from lxml import etree
import pytest


class TestParsers:
    @pytest.mark.parametrize("xml_data,amount,cur_code", [
        ('<TotalAmount CurCode="RUB">6538.00</TotalAmount>', 653800, "RUB"),
        ('<TotalAmount CurCode="RUB">3269.00</TotalAmount>', 326900, "RUB"),
    ])
    def test_parse_amount(self, xml_data, amount, cur_code):
        got = parse_amount(etree.fromstring(xml_data))
        assert got.amount == amount
        assert got.cur_code == cur_code

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

    @pytest.mark.parametrize("xml_data,first_tax,total_amount", [
        (
            '<Price><TaxSummary><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>RI</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YR</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YQ</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>ZZ</TaxCode></Tax></TaxSummary><TotalAmount CurCode="RUB">3269.00</TotalAmount></Price>',
            Tax(Amount(0, None), "RI"), Amount(326900, "RUB")
        ),
    ])
    def test_parse_price(self, xml_data, first_tax, total_amount):
        got = parse_price(etree.fromstring(xml_data))
        assert len(got.taxes) == 4
        for tax in got.taxes:
            assert tax.amount.amount == first_tax.amount.amount
            assert tax.amount.cur_code == first_tax.amount.cur_code
            break
        assert got.total_amount.amount == total_amount.amount

    @pytest.mark.parametrize("xml_data,want", [
        (
            '<FareComponent><CabinType><CabinTypeCode>Economy</CabinTypeCode></CabinType><FareBasisCode>RPROWRF</FareBasisCode><FareRule><RuleCode>PRR1</RuleCode></FareRule><PaxSegmentRefID>2b8e572b-f9d5-4045-8986-1ddd88f2bb66</PaxSegmentRefID><Price><TaxSummary><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YR</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YQ</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>ZZ</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>RI</TaxCode></Tax></TaxSummary><TotalAmount CurCode="RUB">3269.00</TotalAmount></Price><RBD><RBD_Code>R</RBD_Code></RBD></FareComponent>',
            FareComponent("RPROWRF", Price([], Amount(326900, "RUB"))),
        ),
    ])
    def test_parse_fare_componentl(self, xml_data, want):
        got = parse_fare_component(etree.fromstring(xml_data))
        assert got.fare_basis_code == want.fare_basis_code
        assert isinstance(got.price, Price)


    @pytest.mark.parametrize("xml_data,want", [
        (
            '<FareDetail><FareComponent><CabinType><CabinTypeCode>Economy</CabinTypeCode></CabinType><FareBasisCode>RPROWRF</FareBasisCode><FareRule><RuleCode>PRR1</RuleCode></FareRule><PaxSegmentRefID>2b8e572b-f9d5-4045-8986-1ddd88f2bb66</PaxSegmentRefID><Price><TaxSummary><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YR</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>YQ</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>ZZ</TaxCode></Tax><Tax><Amount>0</Amount><QualifierCode>aircompany</QualifierCode><TaxCode>RI</TaxCode></Tax></TaxSummary><TotalAmount CurCode="RUB">3269.00</TotalAmount></Price><RBD><RBD_Code>R</RBD_Code></RBD></FareComponent><PaxRefID>Pax-1</PaxRefID></FareDetail>',
            FareDetail([], "Pax-1"),
        ),
    ])
    def test_parse_fare_detail(self, xml_data, want):
        got = parse_fare_detail(etree.fromstring(xml_data))
        assert isinstance(got.fare_components[0], FareComponent)
        assert got.pax_ref_id == want.pax_ref_id
