# -*- coding: utf-8 -*-
from lxml import etree
import requests

from .utils import lxml_remove_namespace

PROD_GATEWAY = "https://api-test.mixvel.com"
TEST_GATEWAY = "https://api-test.mixvel.com"

class Client:
    def __init__(self,
                 gateway=PROD_GATEWAY, verify_ssl=True):
        """MixVel API Client.

        :param gateway: (optional) gateway url, default is `PROD_GATEWAY`
        :type gateway: str
        :param verify_ssl: (optional) controls whether we verify the server's SSL certificate, defaults to True
        :type verify_ssl: bool
        """
        self.gateway = gateway
        self.verify_ssl = verify_ssl

    def request(self, endpoint,
                message_id=None):
        """Sends request.

        :type correlation_token: uuid.UUID or None
        :return: content of response `Body` node.
        :rtype: lxml.etree._Element
        """
        url = "{gateway}{endpoint}".format(gateway=self.gateway, endpoint=endpoint)
        headers = {
            "Content-Type": "application/xml",
        }
        self.recv = None
        r = requests.post(url,
            headers=headers, verify=self.verify_ssl)
        self.recv = r.content
        r.raise_for_status()
        resp = etree.fromstring(self.recv)
        lxml_remove_namespace(resp)
        err = resp.find("./Body/Error")
        if err is not None:
            msg = "{type}: {code}".format(
                type=err.find("./ErrorType").text,
                code=err.find("./Code").text
            )
            raise IOError(msg)
        return resp.find(".//Body/AppData/")
