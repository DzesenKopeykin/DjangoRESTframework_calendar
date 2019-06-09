from django.db import models
from django.contrib.auth.models import User


REMINDER_HOURS = ((1, '1'), (2, '2'), (3, '4'), (4, '24'), (5, '168'))


class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reminder_hours = models.IntegerField(choices=REMINDER_HOURS)

    class Meta:
        ordering = ('start_datetime',)
