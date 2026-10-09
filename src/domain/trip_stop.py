class TripStop:
    def __init__(
        self,
        trip_stop_id,
        trip_id,
        country,
        city,
        position,
        nights,
    ):
        self.id = trip_stop_id
        self.trip_id = trip_id
        self.country = country
        self.city = city
        self.position = position
        self.nights = nights