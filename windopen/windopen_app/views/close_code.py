import os
import json
import time
import hashlib

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from windopen_app.models import Device
from windopen_starter.log import logger_windopen as log


class GenCloseCode(View):
    @method_decorator(login_required)
    def get(self, request):
        log.info("request path: %s", request.path)
        sep = os.path.sep
        app_path = request.path.strip(sep).split(sep)[0]
        host = request.META.get("HTTP_HOST")
        app_path = host + sep + app_path + sep
        time_salt = time.time()
        uuid = request.GET.get("uuid", "")
        if not uuid:
            return HttpResponse(json.dumps({"close_code": "invalid device uuid `{}`".format(uuid)}))
        close_code = hashlib.sha224("{}{}".format(uuid, time_salt)).hexdigest()
        device = Device.objects.get(uuid=uuid, user=request.user)
        device.close_code = "http://" + app_path + "close_remote" + sep + close_code + sep
        device.save()
        return HttpResponse(json.dumps({"close_code": device.close_code}))
