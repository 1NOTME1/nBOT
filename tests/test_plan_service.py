from services.plan_service import create_plan_item, get_day_plan, remove_plan_item
from domain.plan_item import PlanItem
import pytest

def test_create_plan_item_with_valid_data():
    plan_item = create_plan_item(
        trip_id=1,
        title="Senso-ji",
        date="2027-10-12",
        time="10:00"
    )
    
    assert isinstance(plan_item, PlanItem)
    assert plan_item.trip_id == 1
    assert plan_item.title == "Senso-ji"
    assert plan_item.date == "2027-10-12"
    assert plan_item.time == "10:00"

def test_create_plan_item_with_empty_title():
    with pytest.raises(ValueError):
        create_plan_item(1, "", "2027-10-12", "10:00")

def test_create_plan_item_with_invalid_trip_id():
    with pytest.raises(ValueError):
        create_plan_item(
            plan_item_id=1,
            trip_id=0,
            title="Senso-ji",
            date="2027-10-12",
            time="10:00"
        )


def test_get_day_plan_returns_items_sorted_by_time():
    plan_items = [
        create_plan_item(1, 1, "Dinner", "2027-10-12", "19:00"),
        create_plan_item(2, 1, "Senso-ji", "2027-10-12", "10:00"),
        create_plan_item(3, 1, "Akihabara", "2027-10-12", "14:00"),
    ]

    result = get_day_plan(plan_items, 1, "2027-10-12")

    assert result[0].time == "10:00"
    assert result[1].time == "14:00"
    assert result[2].time == "19:00"


def test_remove_plan_item():
    plan_items = [
        create_plan_item(1, 1, "Senso-ji", "2027-10-12", "10:00"),
        create_plan_item(2, 1, "Akihabara", "2027-10-12", "14:00"),
    ]

    result = remove_plan_item(plan_items, 1)

    assert len(result) == 1
    assert result[0].id == 2