from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # uuid of device
    uuid = models.CharField(max_length=128, unique=True)
    open_code = models.CharField(max_length=512)
    close_code = models.CharField(max_length=512)
    registered = models.DateTimeField(default=now())
    last_seen = models.DateTimeField(default=now())
    active = models.BooleanField(default=None)
    status = models.CharField(max_length=32, default="close")
