# -*- coding: utf-8 -*-
import datetime

from .models import (
    Amount, AnonymousPassenger, Booking, FareComponent,
    FareDetail, MixOrder, Order, OrderItem,
    Price, Service, ServiceOfferAssociations, Tax,
)
from .models import (
    OrderViewResponse,
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
    :rtype: OrderViewResponse
    """
    mix_order = parse_mix_order(resp.find("./Response/MixOrder"))

    return OrderViewResponse(mix_order)


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


def parse_booking(elm):
    """Parses BookingType.

    :param elm: BookingType element
    :type elm: lxml.etree._Element
    :rtype: Booking
    """
    return Booking(elm.find("./BookingID").text)


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


def parse_mix_order(elm):
    """Parses MixOrderType.

    :param elm: MixOrderType element
    :type elm: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = elm.find("./MixOrderID").text
    orders = []
    for order_node in elm.findall("./Order"):
        orders.append(parse_order(order_node))
    total_amount = parse_amount(elm.find("./TotalAmount"))

    return MixOrder(mix_order_id, orders, total_amount)


def parse_order(elm):
    """Parses OrderType.

    :param elm: OrderType element
    :type elm: lxml.etree._Element
    :rtype: Order
    """
    order_id = elm.find("./OrderID").text
    order_items = map(
        lambda node: parse_order_item(node),
        elm.findall("./OrderItem")
    )
    booking_refs = map(
        lambda node: parse_booking(node),
        elm.findall("./BookingRef")
    )
    timelimit = elm.find("./DepositTimeLimitDateTime").text
    timelimit = datetime.datetime.strptime(timelimit, "%Y-%m-%dT%H:%M:%S")
    total_price = parse_price(elm.find("./TotalPrice"))

    return Order(order_id, order_items, booking_refs, timelimit, total_price)

def parse_order_item(elm):
    """Parses OrderItemType.

    :param elm: OrderItemType element
    :type elm: lxml.etree._Element
    :rtype: OrderItem
    """
    order_item_id = elm.find("./OrderItemID").text
    fare_details = []
    for fare_detail_node in elm.findall("./FareDetail"):
        fare_details.append(parse_fare_detail(fare_detail_node))
    price = parse_price(elm.find("./Price"))

    return OrderItem(order_item_id, fare_details, price)


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

def parse_service(elm):
    """Parse ServiceType.
    
    :param elm: Service element
    :type elm: lxml.etree._Element
    """
    service_id = elm.find("./ServiceID").text
    pax_ref_ids = map(lambda ref_id: ref_id.text, elm.findall("./PaxRefID"))
    service_associations = parse_service_offer_associations(elm.find("./ServiceAssociations"))
    validating_party_ref_id = elm.find("./ValidatingPartyRefID").text \
        if elm.find("./ValidatingPartyRefID") is not None else None

    return Service(service_id, pax_ref_ids, service_associations,
        validating_party_ref_id=validating_party_ref_id, validating_party_type=None, pax_types=None)

def parse_service_offer_associations(elm):
    """Parse ServiceOfferAssociationsType.

    :param elm: ServiceOfferAssociations element
    :type elm: lxml.etree._Element
    """
    pax_journey_ref_ids = map(
        lambda ref_id: ref_id.text,
        elm.findall("./PaxJourneyRef/PaxJourneyRefID")
    )

    return ServiceOfferAssociations(
        pax_journey_ref_ids=pax_journey_ref_ids
    )

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
