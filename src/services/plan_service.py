from src.domain.plan_item import PlanItem

def create_plan_item(plan_item_id, trip_id, title, date, time):
    if not isinstance(plan_item_id, int) or isinstance(plan_item_id, bool) or plan_item_id < 1:
        raise ValueError("Invalid plan_item_id")

    if not isinstance(trip_id, int) or isinstance(trip_id, bool) or trip_id < 1:
        raise ValueError("Invalid trip_id")

    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("Invalid title")

    if not isinstance(date, str) or date.strip() == "":
        raise ValueError("Invalid date")

    if not isinstance(time, str) or time.strip() == "":
        raise ValueError("Invalid time")

    return PlanItem(
        plan_item_id=plan_item_id,
        trip_id=trip_id,
        title=title.strip(),
        date=date.strip(),
        time=time.strip()
    )

def remove_plan_item(plan_items, plan_item_id):
    if not isinstance(plan_items, list):
        raise ValueError("Invalid plan_items")

    if not isinstance(plan_item_id, int) or isinstance(plan_item_id, bool) or plan_item_id < 1:
        raise ValueError("Invalid plan_item_id")

    for item in plan_items:
        if item.id == plan_item_id:
            plan_items.remove(item)
            return plan_items

    raise ValueError("Plan item not found")

def update_plan_item(plan_items, plan_item_id, title, date, time):
    if not isinstance(plan_items, list):
        raise ValueError("Invalid plan_items")

    if not isinstance(plan_item_id, int) or isinstance(plan_item_id, bool) or plan_item_id < 1:
        raise ValueError("Invalid plan_item_id")

    if not isinstance(title, str) or title.strip() == "":
        raise ValueError("Invalid title")

    if not isinstance(date, str) or date.strip() == "":
        raise ValueError("Invalid date")

    if not isinstance(time, str) or time.strip() == "":
        raise ValueError("Invalid time")

    for item in plan_items:
        if item.id == plan_item_id:
            item.title = title.strip()
            item.date = date.strip()
            item.time = time.strip()

            return item
    raise ValueError("Plan item not found")