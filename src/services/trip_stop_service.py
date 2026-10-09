from src.domain.trip_stop import TripStop
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def create_trip_stop(
    trip_stops,
    trip_stop_id,
    trip_id,
    country,
    city,
    position,
    nights,
):
    validated_trip_stop_id = validate_positive_int(trip_stop_id)
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)
    validated_city = validate_non_empty_string(city)
    validated_position = validate_positive_int(position)
    
    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    if type(nights) is not int or nights < 0:
        raise ValueError("Invalid nights")
    
    current_stops = get_trip_stops(trip_stops, validated_trip_id)
    if validated_position > len(current_stops) + 1:
        raise ValueError("Invalid position")

    for stop in trip_stops:
        if stop.id == validated_trip_stop_id:
            raise ValueError("Trip stop ID already exists")

    new_stop = TripStop(
        trip_stop_id=validated_trip_stop_id,
        trip_id=validated_trip_id,
        country=validated_country,
        city=validated_city,
        position=validated_position,
        nights=nights,
    )

    current_stops.insert(validated_position - 1, new_stop)

    for position, stop in enumerate(current_stops, start=1):
        stop.position = position

    trip_stops.append(new_stop)

    return new_stop

def get_trip_stops(trip_stops, trip_id):
    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    validated_trip_id = validate_positive_int(trip_id)
    trip_stops_list = []

    for stop in trip_stops:
        if stop.trip_id == validated_trip_id:
            trip_stops_list.append(stop)

    return sorted(trip_stops_list, key=lambda stop : stop.position)

def update_trip_stop(
    trip_stops,
    trip_stop_id,
    country,
    city,
    position,
    nights,
):
    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    validated_trip_stop_id = validate_positive_int(trip_stop_id)
    validated_country = validate_non_empty_string(country)
    validated_city = validate_non_empty_string(city)
    validated_position = validate_positive_int(position)

    if type(nights) is not int or nights < 0:
        raise ValueError("Invalid nights")

    for stop in trip_stops:
        if stop.id == validated_trip_stop_id:
            stop.country = validated_country
            stop.city = validated_city
            stop.position = validated_position
            stop.nights = nights

            return stop
    raise ValueError("Trip stop not found")

def remove_trip_stop(trip_stops, trip_stop_id):
    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    validated_trip_stop_id = validate_positive_int(trip_stop_id)

    for stop in trip_stops:
        if stop.id == validated_trip_stop_id:
            trip_stops.remove(stop)
            _normalize_trip_stop_positions(trip_stops, stop.trip_id)
            return trip_stops
    raise ValueError("Trip stop not found")

def move_trip_stop(trip_stops, trip_stop_id, new_position):
    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    validated_trip_stop_id = validate_positive_int(trip_stop_id)
    validated_new_position = validate_positive_int(new_position)
    target_stop = None
    trip_stops_list = []

    for stop in trip_stops:
        if stop.id == validated_trip_stop_id:
            target_stop = stop
            break
    if target_stop is None:
        raise ValueError("Trip stop not found")

    for stop in trip_stops:
        if stop.trip_id == target_stop.trip_id:
            trip_stops_list.append(stop)
    trip_stops_list = sorted(trip_stops_list, key=lambda stop : stop.position)

    if validated_new_position > len(trip_stops_list):
        raise ValueError("Invalid new position")
    trip_stops_list.remove(target_stop)
    trip_stops_list.insert(validated_new_position - 1, target_stop)

    for position, stop in enumerate(trip_stops_list, start=1):
        stop.position = position
    return trip_stops_list

def _normalize_trip_stop_positions(trip_stops, trip_id):
    validated_trip_id = validate_positive_int(trip_id)

    if not isinstance(trip_stops, list):
        raise ValueError("Invalid data")

    trip_stops_list = []
    for stop in trip_stops:
        if stop.trip_id == validated_trip_id:
            trip_stops_list.append(stop)

    trip_stops_list = sorted(trip_stops_list, key=lambda stop : stop.position)

    for position, stop in enumerate(trip_stops_list, start=1):
        stop.position = position
    return trip_stops_list