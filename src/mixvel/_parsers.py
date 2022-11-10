# -*- coding: utf-8 -*-
import datetime

from .models import (
    Amount, AnonymousPassenger, Booking, DataLists,
    DatedMarketingSegment, FareComponent, FareDetail, MixOrder,
    Offer, OfferItem, Order, OrderItem,
    OriginDest, PaxJourney, PaxSegment, Price,
    RbdAvail, Service, ServiceOfferAssociations, Tax,
    TransportDepArrival, ValidatingParty,
)
from .models import (
    AirShoppingResponse, OrderViewResponse,
)


def is_cancel_success(resp):
    """Checks if cancel order request was successful.

    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: bool
    """
    return all([s == "Success" for s in resp.xpath(".//OperationStatus/text()")])

def parse_air_shopping_response(resp):
    """Parse air shopping response.
    
    :rtype: AirShoppingResponse
    """
    data_lists = DataLists()
    offers = map(
        lambda offer: parse_offer(offer),
        resp.findall("./Response/OffersGroup/CarrierOffers/Offer")
    )

    return AirShoppingResponse(data_lists, offers)

def parse_order_view(resp):
    """Parses order view response.
    
    :param resp: text of Mixvel_OrderCancelRS
    :type resp: lxml.etree._Element
    :rtype: OrderViewResponse
    """
    mix_order = parse_mix_order(resp.find("./Response/MixOrder"))

    return OrderViewResponse(mix_order)

def parse_amount(elm):
    """Parses AmountType.

    :param elm: AmountType element
    :type elm: lxml.etree._Element
    :rtype: Amount
    """
    return Amount(
        int(elm.text.replace(".", "")),
        elm.get("CurCode")
    )

def parse_booking(elm):
    """Parses BookingType.

    :param elm: BookingType element
    :type elm: lxml.etree._Element
    :rtype: Booking
    """
    return Booking(elm.find("./BookingID").text)

def parse_data_lists(elm):
    """Parse DataListsType.

    :param elm: DataListsType element
    :type elm: lxml.etree._Element
    :rtype: DataLists
    """
    origin_dest_list = map(
        lambda elm: parse_origin_dest(elm),
        elm.findall("./OriginDestList/OriginDest")
    )
    pax_journey_list = map(
        lambda elm: parse_pax_journey(elm),
        elm.findall("./PaxJourneyList/PaxJourney")
    )
    validating_party_list = map(
        lambda validating_party: parse_validating_party(validating_party),
        elm.findall("./ValidatingPartyList/ValidatingParty")
    )
    return DataLists(
        origin_dest_list=origin_dest_list,
        pax_journey_list=pax_journey_list,
        validating_party_list=validating_party_list
    )

def parse_dated_marketing_segment(elm):
    """Parse DatedMarketingSegmentType.
    
    :param elm: DatedMarketingSegmentType element
    :type elm: lxml.etree._Element
    :rtype: DatedMarketingSegment
    """
    carrier_code = elm.find("./CarrierDesigCode").text
    flight_number = elm.find("./MarketingCarrierFlightNumberText").text

    return DatedMarketingSegment(carrier_code, flight_number)

def parse_fare_component(elm):
    """Parse FareComponentType.

    :param elm: FareComponentType element
    :type elm: lxml.etree._Element
    :rtype: FareComponent
    """
    fare_basis_code = elm.find("./FareBasisCode").text
    rbd = parse_rbd_avail(elm.find("./RBD"))
    price = parse_price(elm.find("./Price"))

    return FareComponent(fare_basis_code, rbd, price)

def parse_fare_detail(elm):
    """Parses FareDetailType.

    :param elm: FareDetailType element
    :type elm: lxml.etree._Element
    :rtype: FareDetail
    """
    fare_components = []
    for fare_component_node in elm.findall("./FareComponent"):
        fare_components.append(
            parse_fare_component(fare_component_node)
        )
    pax_ref_id = elm.find("./PaxRefID").text

    return FareDetail(fare_components, pax_ref_id)

def parse_mix_order(elm):
    """Parses MixOrderType.

    :param elm: MixOrderType element
    :type elm: lxml.etree._Element
    :rtype: MixOrder
    """
    mix_order_id = elm.find("./MixOrderID").text
    orders = []
    for order_node in elm.findall("./Order"):
        orders.append(parse_order(order_node))
    total_amount = parse_amount(elm.find("./TotalAmount"))

    return MixOrder(mix_order_id, orders, total_amount)

def parse_offer(elm):
    """Parse OfferType.

    :param elm: OfferType element
    :type elm: lxml.etree._Element
    :rtype: OfferItem
    """
    offer_id = elm.find("./OfferID").text
    offer_items = map(
        lambda offer_item: parse_offer_item(offer_item),
        elm.findall("./OfferItem")
    )
    owner_code = elm.find("./OwnerCode").text
    timelimit = elm.find("./OfferExpirationTimeLimitDateTime").text
    timelimit = timelimit.split(".")[0].rstrip('Z')
    timelimit = datetime.datetime.strptime(timelimit, "%Y-%m-%dT%H:%M:%S")

    return Offer(offer_id, offer_items, owner_code, timelimit)

def parse_offer_item(elm):
    """Parse OfferItemType.
    
    :param elm: OfferItemType element
    :type elm: lxml.etree._Element
    :rtype: OfferItem
    """
    offer_item_id = elm.find("./OfferItemID").text
    price = parse_price(elm.find("./Price"))
    services = map(
        lambda service: parse_service(service),
        elm.findall("./Service")
    )
    fare_details = map(
        lambda fare_detail: parse_fare_detail(fare_detail),
        elm.findall("./FareDetail")
    )

    return OfferItem(offer_item_id, price, services,
        fare_details=fare_details)

def parse_order(elm):
    """Parses OrderType.

    :param elm: OrderType element
    :type elm: lxml.etree._Element
    :rtype: Order
    """
    order_id = elm.find("./OrderID").text
    order_items = map(
        lambda node: parse_order_item(node),
        elm.findall("./OrderItem")
    )
    booking_refs = map(
        lambda node: parse_booking(node),
        elm.findall("./BookingRef")
    )
    timelimit = elm.find("./DepositTimeLimitDateTime").text
    timelimit = datetime.datetime.strptime(timelimit, "%Y-%m-%dT%H:%M:%S")
    total_price = parse_price(elm.find("./TotalPrice"))

    return Order(order_id, order_items, booking_refs, timelimit, total_price)

def parse_order_item(elm):
    """Parses OrderItemType.

    :param elm: OrderItemType element
    :type elm: lxml.etree._Element
    :rtype: OrderItem
    """
    order_item_id = elm.find("./OrderItemID").text
    fare_details = []
    for fare_detail_node in elm.findall("./FareDetail"):
        fare_details.append(parse_fare_detail(fare_detail_node))
    price = parse_price(elm.find("./Price"))

    return OrderItem(order_item_id, fare_details, price)

def parse_origin_dest(elm):
    """Parses OriginDestType.

    :param elm: OriginDestType element
    :type elm: lxml.etree._Element
    :rtype: OriginDest
    """
    origin_code = elm.find("./OriginCode").text
    dest_code = elm.find("./DestCode").text
    origin_dest_id = elm.find("./OriginDestID").text \
        if elm.find("./OriginDestID") is not None else None
    pax_journey_ref_ids = map(
        lambda ref_id: ref_id.text,
        elm.findall("./PaxJourneyRefID")
    )

    return OriginDest(origin_code, dest_code,
        origin_dest_id=origin_dest_id, pax_journey_ref_ids=pax_journey_ref_ids)

def parse_pax_journey(elm):
    """Parses PaxJourneyType.
    
    :param elm: PaxJourneyType element
    :type elm: lxml.etree._Element
    :rtype: PaxJourney
    """
    pax_journey_id = elm.find("./PaxJourneyID").text
    pax_segment_ref_ids = map(
        lambda ref_id: ref_id.text,
        elm.findall("./PaxSegmentRefID")
    )

    return PaxJourney(pax_journey_id, pax_segment_ref_ids)

def parse_pax_segment(elm):
    """Parse PaxSegmentType.
    
    :param elm: PaxSegmentType element
    :type elm: lxml.etree._Element
    :rtype: PaxSegment
    """
    pax_segment_id = elm.find("./PaxSegmentID").text
    dep = parse_transport_dep_arrival(elm.find("./Dep"))
    arrival = parse_transport_dep_arrival(elm.find("./Arrival"))
    marketing_carrier_info = \
        parse_dated_marketing_segment(elm.find("./MarketingCarrierInfo"))

    return PaxSegment(pax_segment_id, dep, arrival, marketing_carrier_info)

def parse_price(elm):
    """Parses PriceType.

    :param elm: PriceType element
    :type elm: lxml.etree._Element
    :rtype: Price
    """
    taxes = []
    for tax_node in elm.findall("./TaxSummary/Tax"):
        taxes.append(parse_tax(tax_node))
    total_amount = parse_amount(elm.find("./TotalAmount"))

    return Price(taxes, total_amount)

def parse_rbd_avail(elm):
    """Parse Rbd_Avail_Type.
    
    :param elm: Rbd_Avail_Type element
    :type elm: lxml.etree._Element
    :rtype: RbdAvail
    """
    rbd_code = elm.find("./RBD_Code").text
    availability = int(elm.find("Availability").text) \
        if elm.find("Availability") is not None else None

    return RbdAvail(rbd_code, availability=availability)

def parse_service(elm):
    """Parse ServiceType.
    
    :param elm: ServiceType element
    :type elm: lxml.etree._Element
    :rtype: Service
    """
    service_id = elm.find("./ServiceID").text
    pax_ref_ids = map(lambda ref_id: ref_id.text, elm.findall("./PaxRefID"))
    service_associations = parse_service_offer_associations(elm.find("./ServiceAssociations"))
    validating_party_ref_id = elm.find("./ValidatingPartyRefID").text \
        if elm.find("./ValidatingPartyRefID") is not None else None

    return Service(service_id, pax_ref_ids, service_associations,
        validating_party_ref_id=validating_party_ref_id, validating_party_type=None, pax_types=None)

def parse_service_offer_associations(elm):
    """Parse ServiceOfferAssociationsType.

    :param elm: ServiceOfferAssociations element
    :type elm: lxml.etree._Element
    :rtype: ServiceOfferAssociations
    """
    pax_journey_ref_ids = map(
        lambda ref_id: ref_id.text,
        elm.findall("./PaxJourneyRef/PaxJourneyRefID")
    )

    return ServiceOfferAssociations(
        pax_journey_ref_ids=pax_journey_ref_ids
    )

def parse_tax(elm):
    """Parses TaxType.

    :param elm: TaxType element
    :type elm: lxml.etree._Element
    :rtype: Tax
    """
    return Tax(
        parse_amount(elm.find("./Amount")),
        elm.find("./TaxCode").text
    )

def parse_transport_dep_arrival(elm):
    """Parse TransportDepArrivalType.
    
    :param elm: TransportDepArrivalType element
    :type elm: lxml.etree._Element
    :rtype: TransportDepArrival
    """
    location_code = elm.find("./IATA_LocationCode").text
    scheduled = elm.find("./AircraftScheduledDateTime").text
    scheduled = datetime.datetime.strptime(scheduled, "%Y-%m-%dT%H:%M:%S")

    return TransportDepArrival(location_code, scheduled)

def parse_validating_party(elm):
    """Parse ValidatingPartyType.
    
    :param elm: ValidatingPartyType element
    :type elm: lxml.etree._Element
    :rtype: ValidatingParty
    """
    validating_party_id = elm.find("./ValidatingPartyID").text
    validating_party_code = elm.find("./ValidatingPartyCode").text

    return ValidatingParty(validating_party_id, validating_party_code)
