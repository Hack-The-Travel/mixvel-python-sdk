# -*- coding: utf-8 -*-
import datetime

from .models import (
    Amount, AnonymousPassenger, Booking, MixOrder,
    Order,
)


def parse_amount(s):
    """Parses amount string to int.

    :param s: amount string
    :type s: str
    :rtype: int
    """
    return int(s.replace(".", ""))


def parse_order_view(resp):
    """Parses order view response.
    
    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = resp.find("./Response/MixOrder/MixOrderID").text
    amount = parse_amount(resp.find("./Response/MixOrder/TotalAmount").text)
    amount_cur = resp.find("./Response/MixOrder/TotalAmount").get("CurCode")
    total_amount = Amount(amount, amount_cur)

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

        booking_refs = []
        booking_list_node = order_node.findall("./BookingRef")
        for booking_node in booking_list_node:
            booking_id = booking_node.find("./BookingID").text
            booking_refs.append(Booking(booking_id))

        ttl = order_node.find("./DepositTimeLimitDateTime").text
        ttl = datetime.datetime.strptime(ttl, "%Y-%m-%dT%H:%M:%S")

        orders.append(Order(order_id, booking_refs, ttl))

    return MixOrder(mix_order_id, orders, total_amount)


def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])
