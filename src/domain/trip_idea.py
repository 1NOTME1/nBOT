class TripIdea:
    def __init__(
        self,
        idea_id,
        trip_id,
        country,
        title,
        category,
        city=None,
        notes="",
        status="idea",
        url=None,
    ):
        self.id = idea_id
        self.trip_id = trip_id
        self.country = country
        self.title = title
        self.category = category
        self.city = city
        self.notes = notes
        self.status = status
        self.url = url
        self.voter_ids = set()