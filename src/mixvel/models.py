# -*- coding: utf-8 -*-

"""
mixvel.models
~~~~~~~~~~~~~~~~~~

This module contains the primary objects.
"""

import datetime


class Amount:
    def __init__(self, amount, cur_code):
        """Amount.

        :param amount: amount
        :type amount: int
        :param cur_code: currency code
        :type cur_code: str or None
        """
        self.amount = amount
        self.cur_code = cur_code


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


class FareComponent:
    """Fare component.
    :param fare_basis_code: fare basis code
    :type fare_basis_code: str
    :param price: price
    :type price: Price
    """
    def __init__(self, fare_basis_code, price):
        self.fare_basis_code = fare_basis_code
        self.price = price


class FareDetail:
    def __init__(self, fare_components, pax_ref_id):
        """Fare.

        :param fare_components: fare components
        :type fare_components: list[FareComponent]
        :param pax_ref_id: passenger reference id
        :type pax_ref_id: str
        """
        self.fare_components = fare_components
        self.pax_ref_id = pax_ref_id


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
    def __init__(self, order_id, booking_refs, deposit_timelimit, total_price):
        """Order.
        
        :param order_id: order id
        :type order_id: str
        :param booking_refs: lit of bookings
        :type booking_refs: list[Booking]
        :param deposit_timelimit: ticketing time limit
        :type deposit_timelimit: datetime.datetime
        :param total_price: total price
        :type total_price: Amount
        """
        self.order_id = order_id
        self.booking_refs = booking_refs
        self.deposit_timelimit = deposit_timelimit
        self.total_price = total_price


class OrderItem:
    def __init__(self, order_item_id, fare_details, price):
        """Order item.

        :param order_item_id: order item id
        :type order_item_id: str
        :param fare_details: fare details
        :type fare_details: list[FareDetail]
        :param price: price
        :type price: Price
        """
        self.order_item_id = order_item_id
        self.fare_details = fare_details
        self.price = price


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


class Price:
    def __init__(self, taxes, total_amount):
        """Price.
        
        :param taxes: list of taxes
        :type taxes: list[Tax]
        :param total_amount: total amount
        :type total_amount: Amount
        """
        self.taxes = taxes
        self.total_amount = total_amount


class Tax:
    def __init__(self, amount, tax_code):
        """Tax.
        
        :param amount: amount
        :type amount: Amount
        :param tax_code: tax code
        :type tax_code: str
        """
        self.amount = amount
        self.tax_code = tax_code
