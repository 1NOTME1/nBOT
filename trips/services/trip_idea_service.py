
from django.db import transaction
from django.db.models import Count

from trips.models import TripIdea, TripIdeaVote
from trips.services.trip_service import require_trip_access
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def _get_authorized_idea(idea_id, actor_discord_id):
    validated_idea_id = validate_positive_int(idea_id)

    try:
        idea = TripIdea.objects.get(id=validated_idea_id)
    except TripIdea.DoesNotExist:
        raise ValueError("Trip idea not found") from None

    require_trip_access(idea.trip_id, actor_discord_id)

    return idea


@transaction.atomic
def create_trip_idea(
    trip_id,
    country,
    title,
    category,
    city=None,
    notes="",
    status="idea",
    url=None,
    description="",
    image_url="",
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)
    validated_title = validate_non_empty_string(title)
    validated_category = validate_non_empty_string(category)

    validated_city = (
        validate_non_empty_string(city)
        if city is not None
        else ""
    )

    if not isinstance(notes, str):
        raise ValueError("Invalid notes")
    validated_notes = notes.strip()

    if status not in TripIdea.Status.values:
        raise ValueError("Invalid status")

    validated_url = (
        validate_non_empty_string(url)
        if url is not None
        else ""
    )

    if not isinstance(description, str):
        raise ValueError("Invalid description")
    validated_description = description.strip()

    if not isinstance(image_url, str):
        raise ValueError("Invalid image URL")
    validated_image_url = image_url.strip()

    trip = require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    idea = TripIdea(
        trip=trip,
        country=validated_country,
        title=validated_title,
        category=validated_category,
        city=validated_city,
        notes=validated_notes,
        status=status,
        url=validated_url,
        description=validated_description,
        image_url=validated_image_url,
    )

    idea.full_clean()
    idea.save()

    return idea


def get_trip_ideas(trip_id, *, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        TripIdea.objects.filter(
            trip_id=validated_trip_id
        ).order_by("id")
    )


@transaction.atomic
def update_trip_idea_status(
    idea_id,
    status,
    *,
    actor_discord_id,
):
    if status not in TripIdea.Status.values:
        raise ValueError("Invalid status")

    idea = _get_authorized_idea(
        idea_id,
        actor_discord_id,
    )

    idea.status = status
    idea.save(update_fields=["status"])

    return idea


@transaction.atomic
def remove_trip_idea(idea_id, *, actor_discord_id):
    idea = _get_authorized_idea(
        idea_id,
        actor_discord_id,
    )

    idea.delete()


def get_trip_ideas_by_country(
    trip_id,
    country,
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        TripIdea.objects.filter(
            trip_id=validated_trip_id,
            country__iexact=validated_country,
        ).order_by("id")
    )


def get_trip_ideas_by_city(
    trip_id,
    city,
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)
    validated_city = validate_non_empty_string(city)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        TripIdea.objects.filter(
            trip_id=validated_trip_id,
            city__iexact=validated_city,
        ).order_by("id")
    )


@transaction.atomic
def vote_for_trip_idea(
    idea_id,
    *,
    actor_discord_id,
):
    validated_user_id = validate_positive_int(
        actor_discord_id
    )

    idea = _get_authorized_idea(
        idea_id,
        validated_user_id,
    )

    vote, created = TripIdeaVote.objects.get_or_create(
        idea=idea,
        discord_user_id=validated_user_id,
    )

    if not created:
        raise ValueError("User has already voted")

    return idea


@transaction.atomic
def remove_trip_idea_vote(
    idea_id,
    *,
    actor_discord_id,
):
    validated_user_id = validate_positive_int(
        actor_discord_id
    )

    idea = _get_authorized_idea(
        idea_id,
        validated_user_id,
    )

    try:
        vote = TripIdeaVote.objects.get(
            idea=idea,
            discord_user_id=validated_user_id,
        )
    except TripIdeaVote.DoesNotExist:
        raise ValueError("User has not voted") from None

    vote.delete()

    return idea


def get_top_trip_ideas(
    trip_id,
    *,
    actor_discord_id,
):
    validated_trip_id = validate_positive_int(trip_id)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        TripIdea.objects.filter(
            trip_id=validated_trip_id
        ).annotate(
            vote_count=Count("votes")
        ).order_by("-vote_count", "id")
    )
