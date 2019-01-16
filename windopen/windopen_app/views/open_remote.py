import os
import json

from django.views import View
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

from windopen_app.models import Device, Action
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER


class OpenWindowRemote(View):

    def get(self, request, code):
        log.info("Command: open remote")
        sep = os.path.sep
        app_path = sep.join(request.path.strip(sep).split(sep)[:2])
        host = request.META.get("HTTP_HOST")
        app_path = host + sep + app_path + sep
        log.info("app_path: %s", app_path)
        open_code = "http://" + app_path + code + sep
        log.info("open_code_reverse: %s", open_code)
        try:
            d = Device.objects.get(open_code=open_code)
        except Exception:
            log.error("Device not found %s", open_code)
            raise Http404("Device `{}` not found".format(code))
        if d.status == "open":
            return HttpResponse(json.dumps({"msg": "Already opened"}))
        else:
            user = User.objects.get(username="remote")
            a = Action(device=d, user=user)
            a.action_start = now()
            a.save()
            MTU_SERVER.service.open_window(d.uuid)
        log.info("Command: open remote %s", d.uuid)
        return HttpResponse(json.dumps({"msg": "ok"}))
