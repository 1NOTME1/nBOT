from src.domain.cost_item import CostItem
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
    validate_positive_number,
)


def create_cost_item(
    cost_item_id,
    trip_id,
    plan_item_id,
    title,
    amount,
    currency,
    cost_type,
    category,
):
    validated_cost_item_id = validate_positive_int(cost_item_id)
    validated_trip_id = validate_positive_int(trip_id)
    validated_plan_item_id = None
    
    if plan_item_id is not None:
        validated_plan_item_id = validate_positive_int(plan_item_id)

    validated_title = validate_non_empty_string(title)
    validated_amount = validate_positive_number(amount)
    validated_currency = validate_non_empty_string(currency)

    if cost_type not in ["total", "per_person"]:
        raise ValueError("Invalid cost_type")

    validated_category = validate_non_empty_string(category)

    return CostItem(
        cost_item_id=validated_cost_item_id,
        trip_id=validated_trip_id,
        plan_item_id=validated_plan_item_id,
        title=validated_title,
        amount=validated_amount,
        currency=validated_currency,
        cost_type=cost_type,
        category=validated_category,
    )