
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.db.models import Sum

from trips.models import Trip, PlanItem, CostItem
from trips.services.trip_service import require_trip_access
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
)


def _validate_amount(amount):
    if isinstance(amount, bool) or not isinstance(
        amount, (str, int, Decimal)
    ):
        raise ValueError("Invalid amount")

    try:
        validated_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError):
        raise ValueError("Invalid amount") from None

    if not validated_amount.is_finite() or validated_amount <= 0:
        raise ValueError("Invalid amount")

    return validated_amount


def _validate_cost_fields(
    title,
    amount,
    currency,
    cost_type,
    category,
):
    validated_title = validate_non_empty_string(title)
    validated_amount = _validate_amount(amount)

    validated_currency = validate_non_empty_string(
        currency
    ).upper()

    if (
        len(validated_currency) != 3
        or not validated_currency.isascii()
        or not validated_currency.isalpha()
    ):
        raise ValueError("Invalid currency")

    if cost_type not in CostItem.CostType.values:
        raise ValueError("Invalid cost type")

    validated_category = validate_non_empty_string(category)

    return {
        "title": validated_title,
        "amount": validated_amount,
        "currency": validated_currency,
        "cost_type": cost_type,
        "category": validated_category,
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


def _get_locked_cost_item(cost_item_id, actor_discord_id):
    validated_cost_id = validate_positive_int(cost_item_id)

    try:
        trip_id = CostItem.objects.values_list(
            "trip_id",
            flat=True,
        ).get(id=validated_cost_id)
    except CostItem.DoesNotExist:
        raise ValueError("Cost item not found") from None

    trip = _get_locked_trip(
        trip_id,
        actor_discord_id,
    )

    try:
        cost_item = CostItem.objects.get(
            id=validated_cost_id,
            trip=trip,
        )
    except CostItem.DoesNotExist:
        raise ValueError("Cost item not found") from None

    return cost_item


def _get_plan_item(trip_id, plan_item_id):
    if plan_item_id is None:
        return None

    validated_plan_item_id = validate_positive_int(
        plan_item_id
    )

    try:
        return PlanItem.objects.get(
            id=validated_plan_item_id,
            trip_id=trip_id,
        )
    except PlanItem.DoesNotExist:
        raise ValueError(
            "Plan item not found in this trip"
        ) from None


@transaction.atomic
def create_cost_item(
    trip_id,
    title,
    amount,
    currency,
    cost_type,
    category,
    plan_item_id=None,
    *,
    actor_discord_id,
):
    validated_fields = _validate_cost_fields(
        title,
        amount,
        currency,
        cost_type,
        category,
    )

    trip = _get_locked_trip(
        trip_id,
        actor_discord_id,
    )

    plan_item = _get_plan_item(
        trip.id,
        plan_item_id,
    )

    cost_item = CostItem(
        trip=trip,
        plan_item=plan_item,
        **validated_fields,
    )

    cost_item.full_clean()
    cost_item.save()

    return cost_item


@transaction.atomic
def update_cost_item(
    cost_item_id,
    title,
    amount,
    currency,
    cost_type,
    category,
    plan_item_id=None,
    *,
    actor_discord_id,
):
    validated_fields = _validate_cost_fields(
        title,
        amount,
        currency,
        cost_type,
        category,
    )

    cost_item = _get_locked_cost_item(
        cost_item_id,
        actor_discord_id,
    )

    plan_item = _get_plan_item(
        cost_item.trip_id,
        plan_item_id,
    )

    for field, value in validated_fields.items():
        setattr(cost_item, field, value)

    cost_item.plan_item = plan_item

    cost_item.full_clean()
    cost_item.save()

    return cost_item


@transaction.atomic
def remove_cost_item(
    cost_item_id,
    *,
    actor_discord_id,
):
    cost_item = _get_locked_cost_item(
        cost_item_id,
        actor_discord_id,
    )

    cost_item.delete()


def get_trip_costs(trip_id, *, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        CostItem.objects.filter(
            trip_id=validated_trip_id
        ).select_related("plan_item").order_by("id")
    )


def get_plan_item_costs(plan_item_id, *, actor_discord_id):
    validated_plan_item_id = validate_positive_int(
        plan_item_id
    )

    try:
        plan_item = PlanItem.objects.get(
            id=validated_plan_item_id
        )
    except PlanItem.DoesNotExist:
        raise ValueError("Plan item not found") from None

    require_trip_access(
        plan_item.trip_id,
        actor_discord_id,
    )

    return list(
        CostItem.objects.filter(
            plan_item=plan_item
        ).order_by("id")
    )


def get_trip_cost_summary(trip_id, *, actor_discord_id):
    validated_trip_id = validate_positive_int(trip_id)

    require_trip_access(
        validated_trip_id,
        actor_discord_id,
    )

    return list(
        CostItem.objects.filter(
            trip_id=validated_trip_id
        ).values(
            "currency",
            "cost_type",
        ).annotate(
            total=Sum("amount")
        ).order_by(
            "currency",
            "cost_type",
        )
    )
