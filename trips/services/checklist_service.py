from trips.models import Trip, PlanItem, ChecklistItem
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def create_checklist_item(
    trip_id,
    title,
    plan_item_id=None,
    assigned_to=None,
):
    validated_trip_id = validate_positive_int(trip_id)
    validated_title = validate_non_empty_string(title)

    try:
        trip = Trip.objects.get(id=validated_trip_id)
    except Trip.DoesNotExist:
        raise ValueError("Trip not found") from None

    plan_item = None

    if plan_item_id is not None:
        validated_plan_item_id = validate_positive_int(plan_item_id)

        try:
            plan_item = PlanItem.objects.get(
                id=validated_plan_item_id,
                trip=trip,
            )
        except PlanItem.DoesNotExist:
            raise ValueError("Plan item not found in this trip") from None

    validated_assigned_to = None

    if assigned_to is not None:
        validated_assigned_to = validate_positive_int(assigned_to)

    checklist_item = ChecklistItem(
        trip=trip,
        plan_item=plan_item,
        title=validated_title,
        assigned_to=validated_assigned_to,
        is_done=False,
    )

    checklist_item.full_clean()
    checklist_item.save()

    return checklist_item

def mark_checklist_item_done(checklist_item_id):
    validated_id = validate_positive_int(checklist_item_id)

    try:
        item = ChecklistItem.objects.get(id=validated_id)
    except ChecklistItem.DoesNotExist:
        raise ValueError("Checklist item not found") from None

    item.is_done = True
    item.save(update_fields=["is_done"])

    return item

def mark_checklist_item_undone(checklist_item_id):
    validated_id = validate_positive_int(checklist_item_id)

    try:
        item = ChecklistItem.objects.get(id=validated_id)
    except ChecklistItem.DoesNotExist:
        raise ValueError("Checklist item not found") from None

    item.is_done = False
    item.save(update_fields=["is_done"])

    return item

def assign_checklist_item(checklist_item_id, user_id):
    validated_item_id = validate_positive_int(checklist_item_id)
    validated_user_id = validate_positive_int(user_id)

    try:
        item = ChecklistItem.objects.get(id=validated_item_id)
    except ChecklistItem.DoesNotExist:
        raise ValueError("Checklist item not found") from None

    item.assigned_to = validated_user_id
    item.save(update_fields=["assigned_to"])

    return item

def unassign_checklist_item(checklist_item_id):
    validated_item_id = validate_positive_int(checklist_item_id)

    try:
        item = ChecklistItem.objects.get(id=validated_item_id)
    except ChecklistItem.DoesNotExist:
        raise ValueError("Checklist item not found") from None

    item.assigned_to = None

    item.save(update_fields=["assigned_to"])

    return item


def remove_checklist_item(checklist_item_id):
    validated_item_id = validate_positive_int(checklist_item_id)

    try:
        item = ChecklistItem.objects.get(id=validated_item_id)
    except ChecklistItem.DoesNotExist:
        raise ValueError("Checklist item not found") from None

    item.delete()


def get_trip_checklist(trip_id):
    validated_trip_id = validate_positive_int(trip_id)

    return list(
        ChecklistItem.objects.filter(
            trip_id=validated_trip_id
        ).select_related("plan_item").order_by("id")
    )


def get_plan_item_checklist(plan_item_id):
    validated_plan_item_id = validate_positive_int(plan_item_id)

    return list(
        ChecklistItem.objects.filter(
            plan_item_id=validated_plan_item_id
        ).order_by("id")
    )
