# -*- coding: utf-8 -*-
import os

from mixvel.utils import lxml_remove_namespaces

from lxml import etree

here = os.path.abspath(os.path.dirname(__file__))


def load_response(resp_path,
                  clean_appdata=True):
    """Returns a XML response from the given file."""
    abs_path = os.path.join(here, resp_path)
    resp = etree.parse(abs_path)

    if not clean_appdata:
        return resp

    lxml_remove_namespaces(resp)
    return resp.find('.//Body/AppData/')
