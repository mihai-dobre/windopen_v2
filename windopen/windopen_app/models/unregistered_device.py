from django.utils.timezone import now
from django.db import models


class UnregisteredDevice(models.Model):
    uuid = models.CharField(max_length=32)
    joined = models.DateTimeField(now())
