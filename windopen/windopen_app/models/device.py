from django.db import models
from django.contrib.auth.models import User


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # uuid of device
    uuid = models.CharField(max_length=128, unique=True)
    open_code = models.CharField(max_length=512)
    close_code = models.CharField(max_length=512)
    registered = models.DateTimeField()
    last_seen = models.DateTimeField()
    active = models.BooleanField(default=None)
    status = models.CharField(max_length=32, default="close")

    def __str__(self):
        return "{}".format(self.uuid.title())
