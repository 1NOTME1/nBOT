
from datetime import date as date_type

from django.db import transaction
from django.db.models import F

from trips.models import Trip, TripStop
from trips.services.trip_service import require_trip_access
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
    validate_non_negative_int,
)


def _validate_start_date(start_date):
    if start_date is None:
        return None

    if not isinstance(start_date, str):
        raise ValueError("Invalid start date")

    try:
        return date_type.fromisoformat(start_date)
    except ValueError:
        raise ValueError("Invalid start date") from None


def get_trip_stops(trip_id, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    require_trip_access(validated_trip_id, actor_discord_id)

    return list(
        TripStop.objects.filter(
            trip_id=validated_trip_id
        ).order_by("position", "id")
    )


def _get_locked_stop(trip_stop_id, actor_discord_id):
    try:
        trip_id = TripStop.objects.values_list(
            "trip_id", flat=True
        ).get(id=trip_stop_id)
    except TripStop.DoesNotExist:
        raise ValueError("Trip stop not found") from None

    try:
        Trip.objects.select_for_update().get(id=trip_id)
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None

    require_trip_access(trip_id, actor_discord_id)

    try:
        return TripStop.objects.get(
            id=trip_stop_id,
            trip_id=trip_id,
        )
    except TripStop.DoesNotExist:
        raise ValueError("Trip stop not found") from None


def _move_stop_locked(stop, new_position):
    current_stops = TripStop.objects.filter(
        trip_id=stop.trip_id
    )

    if new_position > current_stops.count():
        raise ValueError("Invalid position")

    old_position = stop.position

    if new_position == old_position:
        return stop

    if new_position < old_position:
        current_stops.filter(
            position__gte=new_position,
            position__lt=old_position,
        ).update(
            position=F("position") + 1
        )
    else:
        current_stops.filter(
            position__gt=old_position,
            position__lte=new_position,
        ).update(
            position=F("position") - 1
        )

    stop.position = new_position
    stop.save(update_fields=["position"])

    return stop


@transaction.atomic
def create_trip_stop(
    trip_id,
    country,
    city,
    position,
    nights,
    start_date=None,
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)
    validated_city = validate_non_empty_string(city)
    validated_position = validate_positive_int(position)
    validated_nights = validate_non_negative_int(nights)
    validated_start_date = _validate_start_date(start_date)

    try:
        trip = Trip.objects.select_for_update().get(
            id=validated_trip_id
        )
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None

    require_trip_access(validated_trip_id, actor_discord_id)

    current_stops = TripStop.objects.filter(trip=trip)

    if validated_position > current_stops.count() + 1:
        raise ValueError("Invalid position")

    current_stops.filter(
        position__gte=validated_position
    ).update(
        position=F("position") + 1
    )

    return TripStop.objects.create(
        trip=trip,
        country=validated_country,
        city=validated_city,
        position=validated_position,
        nights=validated_nights,
        start_date=validated_start_date,
    )


@transaction.atomic
def update_trip_stop(
    trip_stop_id,
    country,
    city,
    position,
    nights,
    start_date=None,
    *,
    actor_discord_id,
):
    validated_trip_stop_id = validate_positive_int(trip_stop_id)
    validated_country = validate_non_empty_string(country)
    validated_city = validate_non_empty_string(city)
    validated_position = validate_positive_int(position)
    validated_nights = validate_non_negative_int(nights)
    validated_start_date = _validate_start_date(start_date)

    # Fetch the stop and verify trip access.
    stop = _get_locked_stop(
        validated_trip_stop_id,
        actor_discord_id,
    )

    # Update the stop's position if necessary.
    stop = _move_stop_locked(
        stop,
        validated_position,
    )

    stop.country = validated_country
    stop.city = validated_city
    stop.nights = validated_nights
    stop.start_date = validated_start_date

    stop.save(
        update_fields=[
            "country",
            "city",
            "nights",
            "start_date",
        ]
    )

    return stop


@transaction.atomic
def remove_trip_stop(
    trip_stop_id,
    *,
    actor_discord_id,
):
    validated_trip_stop_id = validate_positive_int(trip_stop_id)

    stop = _get_locked_stop(
        validated_trip_stop_id,
        actor_discord_id,
    )

    trip_id = stop.trip_id
    deleted_position = stop.position

    stop.delete()

    TripStop.objects.filter(
        trip_id=trip_id,
        position__gt=deleted_position,
    ).update(
        position=F("position") - 1
    )

    return get_trip_stops(trip_id, actor_discord_id)


@transaction.atomic
def move_trip_stop(
    trip_stop_id,
    new_position,
    *,
    actor_discord_id,
):
    validated_trip_stop_id = validate_positive_int(trip_stop_id)
    validated_new_position = validate_positive_int(new_position)

    stop = _get_locked_stop(
        validated_trip_stop_id,
        actor_discord_id,
    )

    _move_stop_locked(stop, validated_new_position)

    return get_trip_stops(stop.trip_id, actor_discord_id)
