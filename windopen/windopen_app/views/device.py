from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.template import RequestContext
from django.shortcuts import render

from windopen_starter.log import logger_windopen as log
from windopen_app.models import Device


class Devices(View):
    @method_decorator(login_required)
    def get(self, request):
        context = RequestContext(request).flatten()
        log.info("USER %s requesting devices.", request.user)
        # u = User.objects.get(username=request.user)
        try:
            devices = Device.objects.filter(user__username=request.user)
        except Exception as err:
            devices = []
            log.exception("No devices registered for user: %s | %s", request.user, err)
        context.update({"devices": devices})
        return render(request, "windopen/devices.html", context=context)
