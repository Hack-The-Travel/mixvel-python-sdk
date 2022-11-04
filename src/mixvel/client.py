# -*- coding: utf-8 -*-
import datetime
from jinja2 import Environment, FileSystemLoader
import logging
from lxml import etree
import os
import requests
import uuid

from mixvel._parsers import (
    is_cancel_success, parse_order_view,
)

from .endpoint import is_login_endpoint, request_template
from .utils import lxml_remove_namespaces

PROD_GATEWAY = "https://api-test.mixvel.com"
TEST_GATEWAY = "https://api-test.mixvel.com"

log = logging.getLogger(__name__)
here = os.path.dirname(os.path.abspath(__file__))


class Client:
    def __init__(self, login, password, structure_unit_id,
                 gateway=PROD_GATEWAY, verify_ssl=True):
        """MixVel API Client.

        :param gateway: (optional) gateway url, default is `PROD_GATEWAY`
        :type gateway: str
        :param verify_ssl: (optional) controls whether we verify the server's SSL certificate, defaults to True
        :type verify_ssl: bool
        """
        self.login = login
        self.password = password
        self.structure_unit_id = structure_unit_id
        self.token = ""
        self.gateway = gateway
        self.verify_ssl = verify_ssl

    def __prepare_request(self, template, context):
        """Constructs request.

        :param template: file name of request template
        :type template: str
        :param context: values for request template rendering
        :type context: dict
        :return: text of rendered request
        :rtype: str
        """
        context["message_id"] = uuid.uuid4()
        context["time_sent"] = datetime.datetime.utcnow()
        template_env = Environment(loader=FileSystemLoader(os.path.join(here, 'templates')))
        request_template = template_env.get_template(template)
        return request_template.render(context)

    def __request(self, endpoint, context):
        """Constructs and executes request.

        :param endpoint: method endpoint, e.g. "/api/Accounts/login"
        :type endpoint: str
        :param context: request variables.
        :type context: dict
        :return: content of response `Body` node.
        :rtype: lxml.etree._Element
        """
        url = "{gateway}{endpoint}".format(gateway=self.gateway, endpoint=endpoint)
        headers = {
            "Content-Type": "application/xml",
        }
        if not is_login_endpoint(endpoint):
            if not self.token:
                self.auth()
            headers["Authorization"] = "Bearer {token}".format(token=self.token)
        template = request_template(endpoint)
        if template is None:
            raise ValueError("Unknown endpoint: {}".format(endpoint))
        data = self.__prepare_request(template, context)
        self.sent = data
        log.info(self.sent)
        self.recv = None
        r = requests.post(url,
            data=data, headers=headers, verify=self.verify_ssl)
        self.recv = r.content
        log.info(self.recv)
        r.raise_for_status()
        resp = etree.fromstring(self.recv)
        lxml_remove_namespaces(resp)
        err = resp.find(".//Error")
        if err is not None:
            raise IOError("{type}: {code}".format(
                type=err.find("./ErrorType").text,
                code=err.find("./Code").text
            ))

        return resp.find(".//Body/AppData/")

    def auth(self):
        """Logins to MixVel API.

        :return: auth token
        :rtype: str
        """
        context = {
            "login": self.login,
            "password": self.password,
            "structure_unit_id": self.structure_unit_id,
        }
        resp = self.__request("/api/Accounts/login", context)
        token = resp.find("./Token").text
        self.token = token

        return token

    def airshopping(self, itinerary, paxes):
        """Executes air shopping request.

        :param itinerary: itinerary
        :type itinerary: list[Leg]
        :param paxes: paxes
        :type paxes: list[AnonymousPassenger]
        """
        context = {
            "itinerary": itinerary,
            "paxes": paxes,
        }
        resp = self.__request("/api/Order/airshopping", context)

        return []

    def create_order(self, paxes):
        """Creates order.

        :param paxes: passengers
        :type paxes: list[Passenger]
        :rtype: OrderViewResponse
        """
        context = {
            "paxes": paxes,
        }
        resp = self.__request("/api/Order/create", context)

        return parse_order_view(resp)

    def retrieve_order(self, mix_order_id):
        """Retrieves order.

        :param mix_order_id: aggregated order id
        :type mix_order_id: str
        :rtype: OrderViewResponse
        """
        context = {
            "mix_order_id": mix_order_id,
        }
        resp = self.__request("/api/Order/retrieve", context)

        return parse_order_view(resp)

    def change_order(self, mix_order_id, amount):
        """Issues tickets.

        :param mix_order_id: aggregated order id
        :type mix_order_id: str
        :param amount: amount
        :type amount: int
        """
        context = {
            "mix_order_id": mix_order_id,
            "amount": amount,
        }
        resp = self.__request("/api/Order/change", context)

    def cancel_order(self, mix_order_id):
        """Cancels order.

        :param mix_order_id: order id
        :type mix_order_id: str
        :rtype: bool
        """
        context = {
            "mix_order_id": mix_order_id,
        }
        resp = self.__request("/api/Order/cancel", context)

        return is_cancel_success(resp)
