# -*- coding: utf-8 -*-
import datetime
import os
import logging

import pytest

from mixvel import (
    TEST_GATEWAY,
    Client,
    Leg,
    AnonymousPassenger,
    SelectedOffer,
    SelectedOfferItem,
    Passenger,
    Individual,
    IdentityDocument,
)

# configure logging to output to console during tests
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_e2e_full_flow():
    login = os.getenv("MIXVEL_LOGIN")
    password = os.getenv("MIXVEL_PASSWORD")
    structure_unit_id = os.getenv("MIXVEL_STRUCTURE_ID")

    if not all([login, password, structure_unit_id]):
        pytest.skip(
            "Skipping test: MIXVEL_LOGIN, MIXVEL_PASSWORD, or MIXVEL_STRUCTURE_ID not set in environment"
        )

    client = Client(login, password, structure_unit_id, gateway=TEST_GATEWAY)
    token = client.auth()
    assert isinstance(token, str)
    assert len(token) > 0
    assert client.token == token

    dept = datetime.datetime.today().date() + datetime.timedelta(days=14)
    itinerary = [
        Leg("MOW", "AER", dept),
        Leg("AER", "MOW", dept + datetime.timedelta(days=8))
    ]
    shopping_paxes = [
        AnonymousPassenger("Pax-1", "ADT"),
        AnonymousPassenger("Pax-2", "ADT"),
        AnonymousPassenger("Pax-3", "CNN"),
    ]
    shopping = client.air_shopping(itinerary, shopping_paxes)
    offers = shopping.offers
    assert len(offers) > 0

    offer = offers[0]
    selected_offer_items = [
        SelectedOfferItem(item.offer_item_id, service.pax_ref_ids)
        for item in offer.offer_items
        for service in item.services
    ]
    selected_offer = SelectedOffer(offer.offer_id, selected_offer_items)
    individuals = [
        Individual("Francis", "Nikolas", "Bacon", "M", datetime.date(1961, 1, 22)),
        Individual("Alice", "Benedict", "Barnham", "F", datetime.date(1992, 1, 1)),
        Individual("Elizabeth", "Francis", "Bacon", "F", datetime.date.today() - datetime.timedelta(days=365 * 10)),
    ]
    docs = [
        IdentityDocument("4509511001", "PS", "RU", datetime.date.today() + datetime.timedelta(days=365 * 10)),
        IdentityDocument("4509511002", "PS", "RU", datetime.date.today() + datetime.timedelta(days=365 * 10)),
        IdentityDocument("4509511003", "PS", "RU", datetime.date.today() + datetime.timedelta(days=365 * 10)),
    ]
    paxes = [
        Passenger("Pax-1", "ADT", individuals[0], docs[0], phone="+79651112233", email="me@francisbacon.com"),
        Passenger("Pax-2", "ADT", individuals[1], docs[1]),
        Passenger("Pax-3", "CNN", individuals[2], docs[2]),
    ]
    order = client.create_order(selected_offer, paxes)
    mix_order_id = order.mix_order.mix_order_id
    total_amount = order.mix_order.total_amount.amount
    assert mix_order_id != ""
    assert total_amount > 0

    retrieve = client.retrieve_order(mix_order_id)
    assert retrieve.mix_order.mix_order_id == mix_order_id

    ticketing = client.change_order(mix_order_id, total_amount / 100)
    assert ticketing.ticket_doc_info

    cancel = client.cancel_order(mix_order_id)
    assert cancel
