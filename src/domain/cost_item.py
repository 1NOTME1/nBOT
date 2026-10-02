class CostItem:
    def __init__(
        self,
        cost_item_id,
        trip_id,
        plan_item_id,
        title,
        amount,
        currency,
        cost_type,
        category,
    ):
        self.id = cost_item_id
        self.trip_id = trip_id
        self.plan_item_id = plan_item_id
        self.title = title
        self.amount = amount
        self.currency = currency
        self.cost_type = cost_type
        self.category = category