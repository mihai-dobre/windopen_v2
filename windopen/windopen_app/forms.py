from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from windopen_app.models import Device


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")


class NewDeviceForm(forms.Form):
    new_device = forms.CharField(required=True, label="Devices\"s serial number", max_length=32)


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ("uuid", "open_code", "close_code", "registered", "last_seen", "active")
