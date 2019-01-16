from django.contrib import admin
from windopen_app.models import UserProfile, Profile, Device, UnregisteredDevice, Action

admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(UnregisteredDevice)
admin.site.register(Action)
