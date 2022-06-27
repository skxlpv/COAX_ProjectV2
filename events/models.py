from datetime import datetime

from django.db import models

from users.models import User


class Event(models.Model):
    TYPES = [
        # may be expanded
        (1, 'Seminar'),
        (2, 'Conference'),
    ]

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250, blank=True, null=True)
    type = models.PositiveIntegerField(choices=TYPES)
    participants = models.ManyToManyField(User, related_name='participants', blank=True, null=True)
    # file upload
    start_time = models.DateTimeField(default=datetime.now(), blank=True, null=True)
    end_time = models.DateTimeField(default=datetime.now(), blank=True, null=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-id']

    def __str__(self):
        return self.title
