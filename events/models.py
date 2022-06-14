from datetime import datetime

from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=150, default='NO TITLE')
    description = models.CharField(max_length=250, default='NO DESCRIPTION')
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-id']

    def __str__(self):
        return self.title
