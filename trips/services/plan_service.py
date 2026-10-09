
from datetime import date as date_type, time as time_type

from django.db import transaction

from trips.models import Trip, TripStop, TripIdea, PlanItem
from trips.services.trip_service import require_trip_access
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def _validate_plan_fields(
    title,
    date,
    time,
    description,
    url,
    image_url,
    duration_minutes,
):
    validated_title = validate_non_empty_string(title)

    try:
        validated_date = date_type.fromisoformat(date)
        validated_time = time_type.fromisoformat(time)
    except (TypeError, ValueError):
        raise ValueError("Invalid date or time") from None

    if validated_time.tzinfo is not None:
        raise ValueError("Time must not include timezone information")

    if not isinstance(description, str):
        raise ValueError("Invalid description")

    if not isinstance(url, str):
        raise ValueError("Invalid URL")

    if not isinstance(image_url, str):
        raise ValueError("Invalid image URL")

    validated_duration = None

    if duration_minutes is not None:
        validated_duration = validate_positive_int(duration_minutes)

    return {
        "title": validated_title,
        "date": validated_date,
        "time": validated_time,
        "description": description.strip(),
        "url": url.strip(),
        "image_url": image_url.strip(),
        "duration_minutes": validated_duration,
    }


def _get_locked_trip(trip_id, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    try:
        trip = Trip.objects.select_for_update().get(
            id=validated_trip_id
        )
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return trip


def _get_locked_plan_item(plan_item_id, actor_discord_id):
    validated_item_id = validate_positive_int(plan_item_id)

    try:
        trip_id = PlanItem.objects.values_list(
            "trip_id", flat=True
        ).get(id=validated_item_id)
    except PlanItem.DoesNotExist:
        raise ValueError("Plan item not found") from None

    _get_locked_trip(trip_id, actor_discord_id)

    try:
        return PlanItem.objects.get(
            id=validated_item_id,
            trip_id=trip_id,
        )
    except PlanItem.DoesNotExist:
        raise ValueError("Plan item not found") from None


def _get_trip_stop(trip_id, trip_stop_id):
    if trip_stop_id is None:
        return None

    validated_stop_id = validate_positive_int(trip_stop_id)

    try:
        return TripStop.objects.get(
            id=validated_stop_id,
            trip_id=trip_id,
        )
    except TripStop.DoesNotExist:
        raise ValueError("Trip stop not found in this trip") from None


def _get_trip_idea(trip_id, trip_idea_id):
    if trip_idea_id is None:
        return None

    validated_idea_id = validate_positive_int(trip_idea_id)

    try:
        return TripIdea.objects.get(
            id=validated_idea_id,
            trip_id=trip_id,
        )
    except TripIdea.DoesNotExist:
        raise ValueError("Trip idea not found in this trip") from None


@transaction.atomic
def create_plan_item(
    trip_id,
    title,
    date,
    time,
    trip_stop_id=None,
    trip_idea_id=None,
    description="",
    url="",
    image_url="",
    duration_minutes=None,
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)

    validated_fields = _validate_plan_fields(
        title,
        date,
        time,
        description,
        url,
        image_url,
        duration_minutes,
    )

    trip = _get_locked_trip(
        validated_trip_id,
        actor_discord_id,
    )

    trip_stop = _get_trip_stop(
        validated_trip_id,
        trip_stop_id,
    )

    trip_idea = _get_trip_idea(
        validated_trip_id,
        trip_idea_id,
    )

    plan_item = PlanItem(
        trip=trip,
        trip_stop=trip_stop,
        trip_idea=trip_idea,
        **validated_fields,
    )

    plan_item.full_clean()
    plan_item.save()

    return plan_item


def get_day_plan(trip_id, date, *, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    try:
        validated_date = date_type.fromisoformat(date)
    except (TypeError, ValueError):
        raise ValueError("Invalid date") from None

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        PlanItem.objects.filter(
            trip_id=validated_trip_id,
            date=validated_date,
        ).select_related(
            "trip_stop",
            "trip_idea",
        ).order_by("time", "id")
    )


@transaction.atomic
def update_plan_item(
    plan_item_id,
    title,
    date,
    time,
    trip_stop_id=None,
    trip_idea_id=None,
    description="",
    url="",
    image_url="",
    duration_minutes=None,
    *,
    actor_discord_id,
):
    validated_fields = _validate_plan_fields(
        title,
        date,
        time,
        description,
        url,
        image_url,
        duration_minutes,
    )

    item = _get_locked_plan_item(
        plan_item_id,
        actor_discord_id,
    )

    trip_stop = _get_trip_stop(
        item.trip_id,
        trip_stop_id,
    )

    trip_idea = _get_trip_idea(
        item.trip_id,
        trip_idea_id,
    )

    item.title = validated_fields["title"]
    item.date = validated_fields["date"]
    item.time = validated_fields["time"]
    item.description = validated_fields["description"]
    item.url = validated_fields["url"]
    item.image_url = validated_fields["image_url"]
    item.duration_minutes = validated_fields["duration_minutes"]

    item.trip_stop = trip_stop
    item.trip_idea = trip_idea

    item.full_clean()
    item.save()

    return item


@transaction.atomic
def remove_plan_item(plan_item_id, *, actor_discord_id):
    item = _get_locked_plan_item(
        plan_item_id,
        actor_discord_id,
    )

    item.delete()


@transaction.atomic
def add_trip_idea_to_plan(
    idea_id,
    date,
    time,
    trip_stop_id=None,
    *,
    actor_discord_id,
):
    validated_idea_id = validate_positive_int(idea_id)

    try:
        trip_id = TripIdea.objects.values_list(
            "trip_id", flat=True
        ).get(id=validated_idea_id)
    except TripIdea.DoesNotExist:
        raise ValueError("Trip idea not found") from None

    _get_locked_trip(trip_id, actor_discord_id)

    try:
        idea = TripIdea.objects.select_for_update().get(
            id=validated_idea_id,
            trip_id=trip_id,
        )
    except TripIdea.DoesNotExist:
        raise ValueError("Trip idea not found") from None

    if idea.status == TripIdea.Status.REJECTED:
        raise ValueError("Rejected trip idea cannot be planned")

    if idea.plan_items.exists():
        raise ValueError("Trip idea is already in the plan")

    plan_item = create_plan_item(
        trip_id=idea.trip_id,
        title=idea.title,
        date=date,
        time=time,
        trip_stop_id=trip_stop_id,
        trip_idea_id=idea.id,
        description=idea.description,
        url=idea.url,
        image_url=idea.image_url,
        actor_discord_id=actor_discord_id,
    )

    if idea.status != TripIdea.Status.SELECTED:
        idea.status = TripIdea.Status.SELECTED
        idea.save(update_fields=["status"])

    return plan_item
