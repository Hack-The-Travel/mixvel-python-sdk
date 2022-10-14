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
