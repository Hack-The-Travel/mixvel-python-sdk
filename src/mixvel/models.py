# -*- coding: utf-8 -*-

"""
mixvel.models
~~~~~~~~~~~~~~~~~~

This module contains the primary objects.
"""

import datetime


class AirShoppingResponse:
    def __init__(self, offers, data_lists):
        """Air Shopping Response
        
        :param offers: list of offers
        :type offers: list[Offer]
        :param data_lists: data lists
        :type data_lists: DataLists
        """
        self.offers = offers
        self.data_lists = data_lists


class OrderViewResponse:
    def __init__(self, mix_order, data_lists, ticket_doc_info=None):
        """Order View Response.
        
        :param mix_order: mix order
        :type mix_order: MixOrder
        :param data_lists: data lists
        :type data_lists: DataLists
        :param ticket_doc_info: ticket doc info
        :type ticket_doc_info: List[TicketDocInfo] or None
        """
        self.mix_order = mix_order
        self.data_lists = data_lists
        self.ticket_doc_info = ticket_doc_info


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


class DataLists:
    def __init__(self, origin_dest_list=None, pax_journey_list=None, pax_segment_list=None,
        validating_party_list=None):
        """Data lists.
        
        :param origin_dest_list: list of origin destinations
        :type origin_dest_list: list[OriginDest]
        :param pax_journey_list: list of passenger journeys
        :type pax_journey_list: list[PaxJourney]
        :param pax_segment_list: list of pax segments
        :type pax_segment_list: list[PaxSegment]
        :param validating_party_list: (optional) list of validating parties
        :type validating_party_list: list[ValidatingParty] or None
        """
        self.origin_dest_list = origin_dest_list
        self.pax_journey_list = pax_journey_list
        self.pax_segment_list = pax_segment_list
        self.validating_party_list = validating_party_list


class DatedMarketingSegment:
    def __init__(self, carrier_desig_code, marketing_carrier_flight_number_text):
        """Dated marketing segment.
        
        :param carrier_desig_code: carrier designator code
        :type carrier_desig_code: str
        :param marketing_carrier_flight_number_text: marketing carrier flight number
        :type marketing_carrier_flight_number_text: str
        """
        self.carrier_desig_code = carrier_desig_code
        self.marketing_carrier_flight_number_text \
            = marketing_carrier_flight_number_text


class FareComponent:
    """Fare component.
    :param fare_basis_code: fare basis code
    :type fare_basis_code: str
    :param rbd: RBD
    :type rbd: RbdAvail
    :param price: price
    :type price: Price
    :param pax_segment_ref_id: passenger segment reference id
    :type pax_segment_ref_id: str
    """
    def __init__(self, fare_basis_code, rbd, price, pax_segment_ref_id):
        self.fare_basis_code = fare_basis_code
        self.rbd = rbd
        self.price = price
        self.pax_segment_ref_id = pax_segment_ref_id


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


class Offer:
    def __init__(self, offer_id, offer_items, owner_code, offer_expiration_timelimit_datetime,
        total_price=None):
        """Offer.

        :param offer_id: offer id
        :type offer_id: str
        :param offer_items: list of offer items
        :type offer_items: list[OfferItem]
        :param owner_code: owner code
        :type owner_code: str
        :param offer_expiration_timelimit_datetime: offer expiration timelimit datetime, in UTC
        :type offer_expiration_timelimit_datetime: datetime.datetime
        :param total_price: (optional) total price
        :type total_price: Price or None
        """
        self.offer_id = offer_id
        self.offer_items = offer_items
        self.owner_code = owner_code 
        self.offer_expiration_timelimit_datetime = offer_expiration_timelimit_datetime
        self.total_price = total_price


class OfferItem:
    def __init__(self, offer_item_id, price, services,
                 fare_details=None):
        """Offer item.

        :param offer_item_id: offer item id
        :type offer_item_id: str
        :param price: price
        :type price: Price
        :param services: list of services
        :type service: list[Service]
        :param fare_details: (optional) fare details
        :type fare_details: list[FareDetail] or None
        """
        self.offer_item_id = offer_item_id
        self.price = price
        self.services = services
        self.fare_details = fare_details


class Order:
    def __init__(self, order_id, order_items, booking_refs,
                 deposit_timelimit, total_price):
        """Order.
        
        :param order_id: order id
        :type order_id: str
        :param order_items: list of order items
        :type order_items: list[OrderItem]
        :param booking_refs: lit of bookings
        :type booking_refs: list[Booking]
        :param deposit_timelimit: ticketing time limit
        :type deposit_timelimit: datetime.datetime
        :param total_price: total price
        :type total_price: Amount
        """
        self.order_id = order_id
        self.order_items = order_items
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


class OriginDest:
    def __init__(self, origin_code, dest_code,
        origin_dest_id=None, pax_journey_ref_ids=None):
        """OriginDest.
        
        :param origin_code: origin code
        :type origin_code: str
        :param dest_code: destination code
        :type dest_code: str
        :param origin_dest_id: (optional) origin destination id
        :type origin_dest_id: str or None
        :param pax_journey_ref_ids: (optional) list of passenger journey reference ids
        :type pax_journey_ref_ids: list[str] or None
        """
        self.origin_code = origin_code
        self.dest_code = dest_code
        self.origin_dest_id = origin_dest_id
        self.pax_journey_ref_ids = pax_journey_ref_ids


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


class PaxJourney:
    def __init__(self, pax_journey_id, pax_segment_ref_ids):
        """PaxJourney.
        
        :param pax_journey_id: passenger journey id
        :type pax_journey_id: str
        :param pax_segment_ref_ids: list of passenger segment reference ids
        :type pax_segment_ref_ids: list[str]
        """
        self.pax_journey_id = pax_journey_id
        self.pax_segment_ref_ids = pax_segment_ref_ids


class PaxSegment:
    def __init__(self, pax_segment_id, dep, arrival, marketing_carrier_info,
        duration=None):
        """PaxSegment.
        
        :param pax_segment_id: passenger segment id
        :type pax_segment_id: str
        :param dep: departure
        :type dep: TransportDepArrival
        :param arrival: arrival
        :type arrival: TransportDepArrival
        :param marketing_carrier_info: marketing carrier info
        :type marketing_carrier_info: DatedMarketingSegment
        :param duration: (optional) duration, e.g. "PT1H30M"
        :type duration: str or None
        """
        self.pax_segment_id = pax_segment_id
        self.dep = dep
        self.arrival = arrival
        self.marketing_carrier_info = marketing_carrier_info
        self.duration = duration  # FIXME: return timdedelta


class Price:
    def __init__(self, tax_summary, total_amount):
        """Price.
        
        :param tax_summary: tax summary
        :type tax_summary: TaxSummary
        :param total_amount: total amount
        :type total_amount: Amount
        """
        # Note.
        # Swagger sample contains of Price element
        # without TaxSummary node
        # 
        # <Price>
		#     <TotalAmount CurCode="RUB">12316</TotalAmount>
		# </Price>
        # 
        # It doesn't conflict with the MixVel openapi specification.
        self.tax_summary = tax_summary
        self.total_amount = total_amount


class RbdAvail:
    def __init__(self, rbd_code, availability=None):
        """RBD Availability.

        :param rbd_code: RBD code
        :type rbd_code: str
        :param availability: (optional) availability
        :type availability: int or None
        """
        self.rbd_code = rbd_code
        self.availability = availability


class SelectedOffer:
    def __init__(self, offer_ref_id, selected_offer_items):
        """Selected offer.

        :param offer_ref_id: offer reference id
        :type offer_ref_id: str
        :param selected_offer_items: list of selected offer items
        :type selected_offer_items: list[SelectedOfferItem]
        """
        self.offer_ref_id = offer_ref_id
        self.selected_offer_items = selected_offer_items


class SelectedOfferItem:
    def __init__(self, offer_item_ref_id, pax_ref_id):
        """Selected offer item.
        
        :param offer_item_ref_id: offer item reference id
        :type offer_item_ref_id: str
        :param pax_ref_id: passenger reference id
        :type pax_ref_id: str
        """
        self.offer_item_ref_id = offer_item_ref_id
        self.pax_ref_id = pax_ref_id


class Service:
    def __init__(self, service_id, pax_ref_ids, service_associations,
                 validating_party_ref_id=None, validating_party_type=None, pax_types=None):
        """Service.
        
        :param service_id: service id
        :type service_id: str
        :param pax_ref_ids: list of passenger reference ids
        :type pax_ref_ids: list[str]
        :param service_associations: service offer associations
        :type service_associations: ServiceOfferAssociations
        :param validating_party_ref_id: (optional) validating party reference id
        :type validating_party_ref_id: str or None
        :param validating_party_type: (optional) validating party type
        :type validating_party_type: ValidatingParty or None
        :param pax_types: (optional) list of pax types
        :type pax_types: list[Passenger] or None
        """
        self.service_id = service_id
        self.pax_ref_ids = pax_ref_ids
        self.service_associations = service_associations
        self.validating_party_ref_id = validating_party_ref_id
        self.validating_party_type = validating_party_type
        self.pax_types = pax_types


class ServiceOfferAssociations:
    def __init__(self, pax_journey_ref_ids=None):
        """ServiceOfferAssociations.

        :param pax_journey_ref_ids: (optional) pax journey reference ids
        :type pax_journey_ref_ids: list[str] or None
        """
        self.pax_journey_ref_ids = pax_journey_ref_ids


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


class TaxSummary:
    def __init__(self, taxes,
        total_tax_amount=None):
        """TaxSummary.
        
        :param taxes: list of taxes
        :type taxes: list[Tax]
        :param total_tax_amount: (optional) total tax amount
        :type total_tax_amount: Amount or None
        """
        self.taxes = taxes
        self.total_tax_amount = total_tax_amount


class TicketDocInfo:
    def __init__(self, pax_ref_id, tickets):
        """TicketDocInfo.

        :param pax_ref_id: pax ref ID
        :type pax_ref_id: str
        :param tickets: tickets
        :type tickets: List[Ticket]
        """
        self.pax_ref_id = pax_ref_id
        self.ticket = tickets


class Ticket:
    def __init__(self, ticket_number):
        """Ticket.
        
        :param ticket_number: ticket number
        :type ticket_number: str
        """
        self.TicketNumber = ticket_number


class TransportDepArrival:
    def __init__(self, iata_location_code, aircraft_scheduled_datetime):
        """TransportDepArrival.
        
        :param iata_location_code: IATA location code
        :type iata_location_code: str
        :param aircraft_scheduled_datetime: aircraft scheduled datetime
        :type aircraft_scheduled_datetime: datetime.datetime
        """
        self.iata_location_code = iata_location_code
        self.aircraft_scheduled_datetime = aircraft_scheduled_datetime


class ValidatingParty:
    def __init__(self, validating_party_id, validating_party_code):
        """Validating party.
        
        :param validating_party_id: validating party id
        :type validating_party_id: str
        :param validating_party_code: validating party code
        :type validating_party_code: str
        """
        self.validating_party_id = validating_party_id
        self.validating_party_code = validating_party_code
