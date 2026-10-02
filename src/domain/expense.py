class Expense:
    def __init__(self, expense_id, trip_id, title, amount, paid_by):
        self.id = expense_id
        self.trip_id = trip_id
        self.title = title
        self.amount = amount
        self.paid_by = paid_by
        self.participants = set()