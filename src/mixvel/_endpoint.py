# -*- coding: utf-8 -*-

"""
mixvel.endpoint
~~~~~~~~~~~~~~
Provides internal functions for working with MixVel API endpoints.
"""

def is_login_endpoint(endpoint):
    """Determines if the given endpoint is the login endpoint.
    
    :param endpoint: endpoint
    :type endpoint: str
    :rtype: bool
    """
    return endpoint == "/api/Accounts/login"


def request_template(endpoint):
    """Returns request template filename for the given endpoint.

    :param endpoint: endpoint
    :type endpoint: str
    :rtype: str or None
    """
    return {
        "/api/Accounts/login": "accounts_login.xml",
        "/api/Order/airshopping": "order_airshopping.xml",
        "/api/Order/create": "order_create.xml",
        "/api/Order/cancel": "order_cancel.xml",
    }.get(endpoint, None)
