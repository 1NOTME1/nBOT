
from django.db import transaction

from trips.models import Trip, TripMember
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def _get_trip(trip_id):
    validated_trip_id = validate_positive_int(trip_id)

    try:
        return Trip.objects.get(id=validated_trip_id)
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None


def _get_owned_trip(trip_id, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)
    validated_actor_id = validate_positive_int(actor_discord_id)

    try:
        trip = Trip.objects.select_for_update().get(
            id=validated_trip_id
        )
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None

    if trip.owner_discord_id != validated_actor_id:
        raise PermissionError("Only the trip owner can perform this action")

    return trip


def create_trip(name, owner_discord_id):
    validated_name = validate_non_empty_string(name)
    validated_owner_id = validate_positive_int(owner_discord_id)

    trip = Trip(
        name=validated_name,
        owner_discord_id=validated_owner_id,
    )

    trip.full_clean()
    trip.save()

    return trip


@transaction.atomic
def rename_trip(trip_id, new_name, actor_discord_id):
    validated_name = validate_non_empty_string(new_name)

    trip = _get_owned_trip(trip_id, actor_discord_id)

    trip.name = validated_name
    trip.full_clean()
    trip.save(update_fields=["name"])

    return trip


@transaction.atomic
def add_member(trip_id, user_id, actor_discord_id):
    validated_user_id = validate_positive_int(user_id)

    trip = _get_owned_trip(trip_id, actor_discord_id)

    if validated_user_id == trip.owner_discord_id:
        raise ValueError("User is already a member")

    member, created = TripMember.objects.get_or_create(
        trip=trip,
        discord_user_id=validated_user_id,
    )

    if not created:
        raise ValueError("User is already a member")

    return member


@transaction.atomic
def remove_member(trip_id, user_id, actor_discord_id):
    validated_user_id = validate_positive_int(user_id)

    trip = _get_owned_trip(trip_id, actor_discord_id)

    if validated_user_id == trip.owner_discord_id:
        raise ValueError("Cannot remove trip owner")

    deleted_count, _ = TripMember.objects.filter(
        trip=trip,
        discord_user_id=validated_user_id,
    ).delete()

    if deleted_count == 0:
        raise ValueError("User is not a member")


def is_trip_member(trip_id, user_id):
    validated_user_id = validate_positive_int(user_id)

    trip = _get_trip(trip_id)

    if trip.owner_discord_id == validated_user_id:
        return True

    return TripMember.objects.filter(
        trip=trip,
        discord_user_id=validated_user_id,
    ).exists()


def require_trip_access(trip_id, user_id):
    validated_user_id = validate_positive_int(user_id)

    trip = _get_trip(trip_id)

    if trip.owner_discord_id == validated_user_id:
        return trip

    has_access = TripMember.objects.filter(
        trip=trip,
        discord_user_id=validated_user_id,
    ).exists()

    if not has_access:
        raise PermissionError("Access denied")

    return trip
