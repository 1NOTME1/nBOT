from domain.trip import Trip

def create_trip(name, owner_id):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Invalid trip name")

    if not isinstance(owner_id, int) or owner_id < 1:
        raise ValueError("Invalid owner_id")

    return Trip(name.strip(), owner_id)

def add_member(trip, user_id):
    if not isinstance(trip, Trip):
        raise ValueError("Invalid trip")

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
        raise ValueError("Invalid user_id")

    if user_id in trip.members:
        raise ValueError("User is already a member")

    trip.members.add(user_id)
    
def remove_member(trip, user_id):
    if not isinstance(trip, Trip):
        raise ValueError("Invalid trip")

    if not isinstance(user_id, int) or isinstance(user_id, bool) or user_id < 1:
        raise ValueError("Invalid user_id")
    
    if user_id == trip.owner_id:
        raise ValueError("Cannot delete owner")
    if user_id not in trip.members:
        raise ValueError("User is not a member")
    
    trip.members.remove(user_id)

def rename_trip(trip, new_name):
    if not isinstance(trip, Trip):
        raise ValueError("Invalid trip")
    
    if not isinstance(new_name, str) or new_name.strip() == "":
        raise ValueError("Invalid name")
    trip.name = new_name.strip()