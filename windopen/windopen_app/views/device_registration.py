import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import now, timedelta

from windopen_app.forms import NewDeviceForm
from windopen_starter.log import logger_windopen as log
from windopen_app.models import Device, UnregisteredDevice, Action


class RegisterDevice(View):
    @method_decorator(login_required)
    def get(self, request):
        form = NewDeviceForm()
        return render(request, "windopen/new_device.html", context={"form": form})

    @method_decorator(login_required)
    def post(self, request):
        form = NewDeviceForm(request.POST)
        if not form.is_valid():
            log.error(dir(form.errors))
            log.error(form.errors["new_device"].data)
            return HttpResponse(
                json.dumps({
                    "status": "error",
                    "msg": form.errors["new_device"][0] if "new_device" in form.errors else form.errors,
                }),
                content_type="application/json",
            )
        else:
            log.info("new_sn: %s", form.cleaned_data)
            new_sn = form.cleaned_data["new_device"]
            # check if the device is already registerd
            existing_device = Device.objects.filter(uuid=new_sn)
            if existing_device:
                log.info("Device `%s` is already registered to user `%s`", new_sn, existing_device[0].user.username)
                status = "error"
                msg = "Device is already registered"
                return HttpResponse(json.dumps({"status": status, "msg": msg}), content_type="application/json")
            # check if the device is connected to the rpyc server and if is in the unregistered table
            unreg_device = UnregisteredDevice.objects.filter(uuid=new_sn)
            if unreg_device:
                d = Device(user=request.user,
                           uuid=new_sn,
                           registered=now(),
                           last_seen=now(),
                           active=True)
                d.save()
                unreg_device.delete()
                status = "success"
                msg = "Successfully registered new device"
                log.info("Registered new device `%s` to user `%s`", new_sn, request.user)
                a = Action(device=d, user=request.user)
                a.status = "close"
                a.action_start = now() - timedelta(5)
                a.action_end = now() - timedelta(5)
                a.save()
                log.info("done creating actions")
            else:
                status = "error"
                msg = "The device is not connected. Please connect the device and check for the green LED"
                log.warning("Device `%s` is not connected.", new_sn)

            return HttpResponse(json.dumps({"status": status, "msg": msg}), content_type="application/json")

