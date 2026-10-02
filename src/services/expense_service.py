from src.domain.expense import Expense
from src.validators.common import (
    validate_positive_int,
    validate_non_empty_string,
    validate_positive_number
)

def create_expense(expense_id, trip_id, title, amount, paid_by):
    validated_expense_id = validate_positive_int(expense_id)
    validated_trip_id = validate_positive_int(trip_id)
    validated_title = validate_non_empty_string(title)
    validated_amount = validate_positive_number(amount)
    validated_paid_by = validate_positive_int(paid_by)
    
    return Expense(
        expense_id=validated_expense_id,
        trip_id=validated_trip_id,
        title=validated_title,
        amount=validated_amount,
        paid_by=validated_paid_by
    )

def add_participant(expense, user_id):
    if not isinstance(expense, Expense):
        raise ValueError("Invalid Expense")
    validated_user_id = validate_positive_int(user_id)
    if validated_user_id in expense.participants:
        raise ValueError("User is already a participant")
    expense.participants.add(validated_user_id)


def remove_participant(expense, user_id):
    if not isinstance(expense, Expense):
        raise ValueError("Invalid Expense")
    validated_user_id = validate_positive_int(user_id)
    if validated_user_id not in expense.participants:
        raise ValueError("User is not a participant")
    expense.participants.remove(validated_user_id)