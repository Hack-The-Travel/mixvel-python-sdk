# -*- coding: utf-8 -*-
import os

from mixvel.utils import lxml_remove_namespaces

from lxml import etree

here = os.path.abspath(os.path.dirname(__file__))


def parse_xml(path):
    """Return an EletementTree object loaded from source path."""
    abs_path = os.path.join(here, path)
    resp = etree.parse(abs_path)
    return resp


def parse_xml_response(resp_path):
    """Return a clean XML API response from the given file."""
    resp = parse_xml(resp_path)
    lxml_remove_namespaces(resp)
    return resp.find('.//Body/AppData/')
