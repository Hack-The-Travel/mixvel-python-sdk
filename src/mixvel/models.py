# -*- coding: utf-8 -*-

"""
mixvel.models
~~~~~~~~~~~~~~~~~~

This module contains the primary objects.
"""

class AnonymousPassenger:
    def __init__(self, ptc):
        """Anonymous passenger.

        :param ptc: passenger type code, e.g. "ADT", "CNN", etc.
        :param ptc: str
        """
        self.ptc = ptc


class Individual():
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
        :type birthdate: datetime.datetime
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
        :param departure: departure datetime
        :type departure: datetime.datetime
        :param cabin: (optional) cabin, default is "Economy"
        :type cabin: str
        """
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.cabin = cabin
