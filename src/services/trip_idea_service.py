from src.domain.trip_idea import TripIdea
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)
from src.services.plan_service import create_plan_item


def create_trip_idea(
    idea_id,
    trip_id,
    country,
    title,
    category,
    city=None,
    notes="",
    status="idea",
    url=None,
):
    validated_idea_id = validate_positive_int(idea_id)
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)
    validated_title = validate_non_empty_string(title)
    validated_category = validate_non_empty_string(category)

    validated_city = None
    if city is not None:
        validated_city = validate_non_empty_string(city)

    if not isinstance(notes, str):
        raise ValueError("Invalid notes")
    validated_notes = notes.strip()

    if status not in ("idea", "selected", "rejected"):
        raise ValueError("Invalid status")

    validated_url = None
    if url is not None:
        validated_url = validate_non_empty_string(url)

    return TripIdea(
        idea_id=validated_idea_id,
        trip_id=validated_trip_id,
        country=validated_country,
        title=validated_title,
        category=validated_category,
        city=validated_city,
        notes=validated_notes,
        status=status,
        url=validated_url,
    )

def get_trip_ideas(trip_ideas, trip_id):
    validated_trip_id = validate_positive_int(trip_id)
    trip_ideas_list = []

    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")

    for ideas in trip_ideas:
        if ideas.trip_id == validated_trip_id:
            trip_ideas_list.append(ideas)

    return trip_ideas_list

def update_trip_idea_status(trip_ideas, idea_id, status):
    validated_idea_id = validate_positive_int(idea_id)

    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")

    if status not in ["idea", "selected", "rejected"]:
        raise ValueError("Invalid status")

    for idea in trip_ideas:
        if idea.id == validated_idea_id:
            idea.status = status
            return idea

    raise ValueError("Trip idea not found")

def remove_trip_idea(trip_ideas, idea_id):
    validated_idea_id = validate_positive_int(idea_id)

    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")

    for idea in trip_ideas:
        if idea.id == validated_idea_id:
            trip_ideas.remove(idea)
            return trip_ideas

    raise ValueError("Trip idea not found")

def get_trip_ideas_by_country(trip_ideas, trip_id, country):
    validated_trip_id = validate_positive_int(trip_id)
    validated_country = validate_non_empty_string(country)
    trip_ideas_list = []
    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")
    for idea in trip_ideas:
        if idea.trip_id == validated_trip_id and idea.country.casefold() == validated_country.casefold():
            trip_ideas_list.append(idea)
    return trip_ideas_list

def get_trip_ideas_by_city(trip_ideas, trip_id, city):
    validated_trip_id = validate_positive_int(trip_id)
    validated_city = validate_non_empty_string(city)
    trip_ideas_list = []

    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")

    for idea in trip_ideas:
        if (
            idea.trip_id == validated_trip_id
            and idea.city is not None
            and idea.city.casefold() == validated_city.casefold()
        ):
            trip_ideas_list.append(idea)

    return trip_ideas_list



def add_trip_idea_to_plan(
    trip_ideas,
    idea_id,
    plan_item_id,
    date,
    time,
):
    if not isinstance(trip_ideas, list):
        raise ValueError("Invalid data")

    validated_idea_id = validate_positive_int(idea_id)

    for idea in trip_ideas:
        if idea.id == validated_idea_id:
            plan_item = create_plan_item(plan_item_id, idea.trip_id, idea.title, date, time)
            idea.status = "selected"
            return plan_item
    raise ValueError("Trip idea not found")