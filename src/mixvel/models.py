# -*- coding: utf-8 -*-

"""
mixvel.models
~~~~~~~~~~~~~~~~~~

This module contains the primary objects.
"""

import datetime


class Amount:
    def __init__(self, amount, currency):
        """Amount.

        :param amount: amount
        :type amount: int
        :param currency: currency
        :type currency: str
        """
        self.amount = amount
        self.currency = currency


class AnonymousPassenger:
    def __init__(self, pax_id, ptc):
        """Anonymous passenger.

        :param pax_id: passenger id
        :type pax_id: str
        :param ptc: passenger type code, e.g. "ADT", "CNN", etc.
        :param ptc: str
        """
        self.pax_id = pax_id
        self.ptc = ptc


class Booking:
    def __init__(self, booking_id):
        """Booking.

        :param booking_id: booking id
        :type booking_id: str
        """
        self.booking_id = booking_id


class IdentityDocument:
    def __init__(self, doc_id, type_code, issuing_country_code, expiry_date):
        """Identity document.

        :param doc_id: document ID
        :type doc_id: str
        :param type_code: document type code, e.g. "PS"
        :type type_code: str
        :param issuing_country_code: issuing country code, e.g. "RU"
        :type issuing_country_code: str
        :param expiry_date: document expiry date
        :type expiry_date: datetime.date
        """
        self.doc_id = doc_id
        self.type_code = type_code
        self.issuing_country_code = issuing_country_code
        self.expiry_date = expiry_date


class Individual:
    def __init__(self, given_name, middle_name, surname,
                 gender, birthdate):
        """Individual.

        :param given_name: given name
        :type given_name: str
        :param middle_name: middle name
        :type middle_name: str
        :param surname: surname
        :type surname: str
        :param gender: gender, possible values: "M", "F"
        :type gender: str
        :param birthdate: birthdate
        :type birthdate: datetime.date
        """
        self.given_name = given_name
        self.middle_name = middle_name
        self.surname = surname
        self.gender = gender
        self.birthdate = birthdate


class Leg:
    def __init__(self, origin, destination, departure,
                 cabin="Economy"):
        """Flight leg.

        :param origin: origin
        :type origin: str
        :param destination: destination
        :type destination: str
        :param departure: departure date
        :type departure: datetime.date
        :param cabin: (optional) cabin, default is "Economy"
        :type cabin: str
        """
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.cabin = cabin


class MixOrder:
    def __init__(self, mix_order_id, orders, total_amount):
        """MixOrder.

        :param mix_order_id: mix order id
        :type mix_order_id: str
        :param orders: list of orders
        :type orders: list[Order]
        :param total_amount: total amount
        :type total_amount: Amount
        """
        self.mix_order_id = mix_order_id
        self.orders = orders
        self.total_amount = total_amount


class Order:
    def __init__(self, order_id, booking_refs, relevance_datetime):
        """Order.
        
        :param order_id: order id
        :type order_id: str
        :param booking_refs: lit of bookings
        :type booking_refs: list[Booking]
        :param relevance_datetime: ticketing time limit
        :type relevance_datetime: datetime.datetime
        """
        self.order_id = order_id
        self.booking_refs = booking_refs
        self.relevance_datetime = relevance_datetime


class Passenger(AnonymousPassenger):
    def __init__(self, pax_id, ptc, individual, doc,
                 phone=None, email=None):
        """Passenger.

        :param pax_id: passenger id
        :type pax_id: str
        :param ptc: passenger type code, e.g. "ADT", "CNN", etc.
        :param ptc: str
        :param individual: individual
        :type individual: Individual
        :param doc: identity document
        :type doc: IdentityDocument
        :param phone: (optional) contact phone number
        :param phone: str or None
        :param email: (optional) contact email
        :param email: str or None
        """
        AnonymousPassenger.__init__(self, pax_id, ptc)
        self.individual = individual
        self.doc = doc
        self.phone = phone
        self.email = email
