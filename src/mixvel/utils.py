# -*- coding: utf-8 -*-

"""
mixvel.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within mixvel
that are also useful for external consumption.
"""

from lxml import objectify
from lxml import etree


def lxml_remove_namespaces(root):
    """Remove all namespaces and prefixes from lxml object.

    Links:
    * https://stackoverflow.com/a/18160164/7309986

    :param root: XML object
    :type root: lxml.etree._Element
    """
    for elem in root.getiterator():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]
    objectify.deannotate(root, cleanup_namespaces=True)
