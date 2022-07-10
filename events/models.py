from django.db import models

from hospitals.models import Hospital
from users.models import User


class Event(models.Model):
    SEMINAR = 'SM'
    CONFERENCE = 'CN'
    ANOTHER = 'AN'
    options = (
        (SEMINAR, 'Seminar'),
        (CONFERENCE, 'Conference'),
        (ANOTHER, 'Another')
    )

    title = models.CharField(max_length=150, blank=False, null=False)
    type = models.PositiveIntegerField(choices=options, blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, default='')

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
