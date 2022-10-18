# -*- coding: utf-8 -*-
def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])
