from services.plan_service import create_plan_item
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
        create_plan_item(0, "Senso-ji", "2027-10-12", "10:00")