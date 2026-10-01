from services.trip_service import create_trip
from domain.trip import Trip
import pytest

def test_create_trip_with_valid_data():
    trip = create_trip("Japan 2027", 123)
    
    assert isinstance(trip, Trip)
    assert trip.name == "Japan 2027"
    assert trip.owner_id == 123
    
def test_create_trip_with_empty_name():
    with pytest.raises(ValueError):
        create_trip("", 123)

def test_create_trip_with_spaces_in_name():
    with pytest.raises(ValueError):
        create_trip("  ", 123)

def test_create_trip_with_incorrect_name():
    with pytest.raises(ValueError):
        create_trip(123, 123)

def test_create_trip_with_incorrect_owner_id():
    with pytest.raises(ValueError):
        create_trip("Japan", 0)

def test_create_trip_with_incorrect_owner_id_type():
    with pytest.raises(ValueError):
        create_trip("Japan", "123")

def test_create_trip_trims_name():
    trip = create_trip("  Japan  ", 123)
    
    assert trip.name == "Japan"