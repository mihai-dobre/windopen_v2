from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from .device import Device


class Action(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, to_field="uuid")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    action_start = models.DateTimeField(default=now())
    action_end = models.DateTimeField(default=now())

    class Meta:
        ordering = ["action_start"]
