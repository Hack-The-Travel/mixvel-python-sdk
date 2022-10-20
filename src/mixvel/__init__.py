# -*- coding: utf-8 -*-
from .__version__ import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__,
)

from . import utils
from .client import PROD_GATEWAY, TEST_GATEWAY
from .client import Client
from .models import (
    Amount, AnonymousPassenger, Booking, IdentityDocument,
    Individual, Leg, MixOrder, Order,
    Passenger,
)
from . import parsers

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
