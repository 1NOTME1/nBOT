from domain.trip import Trip

def create_trip(name, owner_id):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Invalid trip name")

    if not isinstance(owner_id, int) or owner_id < 1:
        raise ValueError("Invalid owner_id")

    return Trip(name.strip(), owner_id)