# -*- coding: utf-8 -*-
from .__version__ import (
    __title__, __description__, __url__, __version__,
    __author__, __author_email__,
)

from . import utils
from .client import PROD_GATEWAY, TEST_GATEWAY
from .client import Client
from .models import (
    Amount, AnonymousPassenger, Booking, FareComponent,
    FareDetail, IdentityDocument, Individual, Leg,
    MixOrder, Order, OrderItem, Passenger,
    Price, Tax,
)  # types
from .models import (
    OrderViewResponse,
)  # responses

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
