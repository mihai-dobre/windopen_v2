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


class GenOpenCode(View):
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
            return HttpResponse(json.dumps({"open_code": "invalid device uuid `{}`".format(uuid)}))
        open_code = hashlib.sha224("{}{}".format(uuid, time_salt).encode(encoding="UTF-8")).hexdigest()
        device = Device.objects.get(uuid=uuid, user=request.user)
        device.open_code = "http://" + app_path + "open_remote" + sep + open_code + sep
        device.save()
        return HttpResponse(json.dumps({"open_code": device.open_code}))
