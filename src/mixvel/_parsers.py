# -*- coding: utf-8 -*-
import datetime

from .models import (
    Amount, AnonymousPassenger, Booking, FareComponent,
    FareDetail, MixOrder, Order, Price,
    Tax,
)


def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])


def parse_order_view(resp):
    """Parses order view response.
    
    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = resp.find("./Response/MixOrder/MixOrderID").text
    total_amount = parse_amount(resp.find("./Response/MixOrder/TotalAmount"))

    paxes = []
    pax_list_node = resp.find("./Response/DataLists/PaxList")
    for pax_node in pax_list_node:
        paxes.append(
            AnonymousPassenger(
                pax_node.find("./PaxID").text,
                pax_node.find("./PTC").text
            )
        )

    orders = []
    orders_node = resp.findall("./Response/MixOrder/Order")
    for order_node in orders_node:
        order_id = order_node.find("./OrderID").text
        amount = parse_amount(order_node.find("./TotalPrice/TotalAmount"))

        booking_refs = []
        booking_list_node = order_node.findall("./BookingRef")
        for booking_node in booking_list_node:
            booking_id = booking_node.find("./BookingID").text
            booking_refs.append(Booking(booking_id))

        ttl = order_node.find("./DepositTimeLimitDateTime").text
        ttl = datetime.datetime.strptime(ttl, "%Y-%m-%dT%H:%M:%S")

        orders.append(Order(order_id, booking_refs, ttl, amount))

    return MixOrder(mix_order_id, orders, total_amount)


def parse_amount(elm):
    """Parses AmountType.

    :param elm: AmountType element
    :type elm: lxml.etree._Element
    :rtype: Amount
    """
    return Amount(
        int(elm.text.replace(".", "")),
        elm.get("CurCode")
    )


def parse_fare_component(elm):
    """Parses FareComponentType.

    :param elm: FareComponentType element
    :type elm: lxml.etree._Element
    :rtype: FareComponent
    """
    return FareComponent(
        elm.find("./FareBasisCode").text,
        parse_price(elm.find("./Price"))
    )


def parse_fare_detail(elm):
    """Parses FareDetailType.

    :param elm: FareDetailType element
    :type elm: lxml.etree._Element
    :rtype: FareDetail
    """
    fare_components = []
    for fare_component_node in elm.findall("./FareComponent"):
        fare_components.append(
            parse_fare_component(fare_component_node)
        )
    pax_ref_id = elm.find("./PaxRefID").text

    return FareDetail(fare_components, pax_ref_id)


def parse_price(elm):
    """Parses PriceType.

    :param elm: PriceType element
    :type elm: lxml.etree._Element
    :rtype: Price
    """
    taxes = []
    for tax_node in elm.findall("./TaxSummary/Tax"):
        taxes.append(parse_tax(tax_node))
    total_amount = parse_amount(elm.find("./TotalAmount"))

    return Price(taxes, total_amount)


def parse_tax(elm):
    """Parses TaxType.

    :param elm: TaxType element
    :type elm: lxml.etree._Element
    :rtype: Tax
    """
    return Tax(
        parse_amount(elm.find("./Amount")),
        elm.find("./TaxCode").text
    )
