# -*- coding: utf-8 -*-
import os

import pytest
from lxml import etree

from mixvel.utils import lxml_remove_namespace


here = os.path.abspath(os.path.dirname(__file__))


class TestUtils:
    @pytest.mark.parametrize('response_file_path', [
        os.path.join(here, 'responses/accounts/', 'login.xml'),
    ])
    def test_lxml_remove_namespace(self, response_file_path):
        response = etree.parse(response_file_path)
        assert response.find('.//AuthResponse') is None
        lxml_remove_namespace(response)
        assert response.find('.//AuthResponse') is not None
