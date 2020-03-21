from django.db import models

from core.models import Stop


class Connection(models.Model):
    stop = models.ManyToManyField(Stop)
    duration = models.DurationField(blank=True, null=True)
