from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.template import RequestContext
from django.shortcuts import render

from windopen_starter.log import logger_windopen as log
from windopen_app.models import Device


class Device(View):
    @method_decorator(login_required)
    def get(self, request):
        context = RequestContext(request).flatten()
        try:
            devices = Device.objects.filter(user=request.user)
        except Exception as err:
            devices = []
            log.warning("No devices registered for user: %s | %s", request.user, err)
        context.update({"devices": devices})
        return render(request, "windopen/devices.html", context=context)
