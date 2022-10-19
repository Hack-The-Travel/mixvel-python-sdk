# -*- coding: utf-8 -*-
import datetime

from .models import MixOrder


def parse_order_view(resp):
    """Parses order view response.
    
    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = resp.find("./Response/MixOrder/MixOrderID").text
    booking_id = resp.find("./Response/MixOrder/Order/BookingRef/BookingID").text
    time_limit = resp.find("./Response/MixOrder/Order/DepositTimeLimitDateTime").text
    time_limit = datetime.datetime.strptime(time_limit, "%Y-%m-%dT%H:%M:%S")

    return MixOrder(mix_order_id, booking_id, time_limit)


def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])
