# -*- coding: utf-8 -*-

"""
mixvel.models
~~~~~~~~~~~~~~~~~~

This module contains the primary objects.
"""

import datetime


class AnonymousPassenger:
    def __init__(self, ptc):
        """Anonymous passenger.

        :param ptc: passenger type code, e.g. "ADT", "CNN", etc.
        :param ptc: str
        """
        self.ptc = ptc


class Contact:
    def __init__(self, email, phone):
        """Contact information.

        :param email: (optional) contact email
        :param email: str or None
        :param phone: (optional) contact phone number
        :param phone: str or None
        """
        self.email = email
        self.phone = phone


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
