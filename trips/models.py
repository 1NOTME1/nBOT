from django.db import models


class Trip(models.Model):
    name = models.CharField(max_length=200)
    owner_discord_id = models.PositiveBigIntegerField()

    def __str__(self):
        return self.name

class TripStop(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="stops",
    )
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    position = models.PositiveIntegerField()
    nights = models.PositiveIntegerField(default=0)
    start_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.position}. {self.city}"

class TripIdea(models.Model):
    class Status(models.TextChoices):
        IDEA = "idea", "Idea"
        SELECTED = "selected", "Selected"
        REJECTED = "rejected", "Rejected"

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="ideas",
    )

    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IDEA,
    )
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class TripIdeaVote(models.Model):
    idea = models.ForeignKey(
        TripIdea,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    discord_user_id = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["idea", "discord_user_id"],
                name="unique_trip_idea_vote",
            )
        ]

class PlanItem(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="plan_items",
    )

    trip_stop = models.ForeignKey(
        TripStop,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan_items",
    )

    trip_idea = models.ForeignKey(
        TripIdea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan_items",
    )

    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    image_url = models.URLField(blank=True)
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.date} {self.time} - {self.title}"

class ChecklistItem(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="checklist_items",
    )

    plan_item = models.ForeignKey(
        PlanItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="checklist_items",
    )

    title = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)

    assigned_to = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title

class TripMember(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="members",
    )

    discord_user_id = models.PositiveBigIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "discord_user_id"],
                name="unique_trip_member",
            )
        ]

    def __str__(self):
        return f"{self.discord_user_id} - {self.trip.name}"
    

class CostItem(models.Model):
    class CostType(models.TextChoices):
        TOTAL = "total", "Total"
        PER_PERSON = "per_person", "Per person"

    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="cost_items",
    )

    plan_item = models.ForeignKey(
        PlanItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cost_items",
    )

    title = models.CharField(max_length=200)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    currency = models.CharField(max_length=3)

    cost_type = models.CharField(
        max_length=20,
        choices=CostType.choices,
    )

    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.amount} {self.currency}"
