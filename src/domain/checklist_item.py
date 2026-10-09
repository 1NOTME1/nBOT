class ChecklistItem:
    def __init__(self, checklist_item_id, trip_id, title, is_done=False, assigned_to=None):
        self.id = checklist_item_id
        self.trip_id = trip_id
        self.title = title
        self.is_done = is_done
        self.assigned_to = assigned_to