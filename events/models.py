from django.db import models

from hospitals.models import Hospital
from users.models import User


class Event(models.Model):
    SEMINAR = "SM"
    CONFERENCE = "CN"
    OTHER = "OT"

    options = (
        (SEMINAR, "Seminar"),
        (CONFERENCE, "Conference"),
        (OTHER, "Other")
    )

    title = models.CharField(max_length=150, blank=False, null=False)
    type = models.CharField(max_length=2, choices=options, default=OTHER, blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    description = models.CharField(max_length=250, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-id']

    def __str__(self):
        return self.title
