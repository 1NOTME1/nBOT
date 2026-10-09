from validators.common import validate_positive_int, validate_non_empty_string
from domain.checklist_item import ChecklistItem

def create_checklist_item(checklist_item_id, trip_id, title, assigned_to=None):
    validated_checklist_item_id = validate_positive_int(checklist_item_id)
    validated_trip_id = validate_positive_int(trip_id)
    validated_title = validate_non_empty_string(title)

    if assigned_to is not None:
        validate_positive_int(assigned_to)

    return ChecklistItem(
        checklist_item_id=validated_checklist_item_id,
        trip_id=validated_trip_id,
        is_done=False,
        title=validated_title,
        assigned_to=assigned_to
    )

def mark_checklist_item_done(checklist_items, checklist_item_id):
    validated_checklist_item_id = validate_positive_int(checklist_item_id)

    if not isinstance(checklist_items, list):
        raise ValueError("Invalid data")

    for item in checklist_items:
        if item.id  == validated_checklist_item_id:
            item.is_done = True
            return item
    raise ValueError("Checklist item not found")

def mark_checklist_item_undone(checklist_items, checklist_item_id):
    validated_checklist_item_id = validate_positive_int(checklist_item_id)

    if not isinstance(checklist_items, list):
        raise ValueError("Invalid data")

    for item in checklist_items:
        if item.id  == validated_checklist_item_id:
            item.is_done = False
            return item
    raise ValueError("Checklist item not found")

def assign_checklist_item(checklist_items, checklist_item_id, user_id):
    validated_checklist_item_id = validate_positive_int(checklist_item_id)
    validated_user_id = validate_positive_int(user_id)

    if not isinstance(checklist_items, list):
        raise ValueError("Invalid data")

    for item in checklist_items:
        if item.id  == validated_checklist_item_id:
            item.assigned_to = validated_user_id
            return item
    raise ValueError("Checklist item not found")

def remove_checklist_item(checklist_items, checklist_item_id):
    validated_checklist_item_id = validate_positive_int(checklist_item_id)

    if not isinstance(checklist_items, list):
        raise ValueError("Invalid data")

    for item in checklist_items:
        if item.id == validated_checklist_item_id:
            checklist_items.remove(item)
            return checklist_items
    raise ValueError("Checklist item not found")

def get_trip_checklist(checklist_items, trip_id):
    trip_checklist = []
    
    validated_trip_id = validate_positive_int(trip_id)

    if not isinstance(checklist_items, list):
        raise ValueError("Invalid data")

    for item in checklist_items:
        if item.trip_id == validated_trip_id:
            trip_checklist.append(item)
            
    return trip_checklist