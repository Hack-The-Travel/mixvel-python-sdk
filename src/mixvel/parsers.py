# -*- coding: utf-8 -*-
import datetime

from .models import (
    AnonymousPassenger, MixOrder,
)


def parse_order_view(resp):
    """Parses order view response.
    
    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = resp.find("./Response/MixOrder/MixOrderID").text

    paxes = []
    pax_list_node = resp.find("./Response/DataLists/PaxList")
    for pax_node in pax_list_node:
        paxes.append(
            AnonymousPassenger(
                pax_node.find("./PaxID").text,
                pax_node.find("./PTC").text
            )
        )

    order_node = resp.find("./Response/MixOrder/Order")
    booking_id = order_node.find("./BookingRef/BookingID").text
    time_limit = order_node.find("./DepositTimeLimitDateTime").text
    time_limit = datetime.datetime.strptime(time_limit, "%Y-%m-%dT%H:%M:%S")

    return MixOrder(mix_order_id, booking_id, time_limit)


def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])
