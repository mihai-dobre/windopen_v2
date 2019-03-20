import os
import json

from django.views import View
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User

from windopen_app.models import Device, Action
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER, RPYC_SERVER_THREAD


class CloseWindowRemote(View):
    def get(self, request, code):
        log.info("Command: close remote")
        sep = os.path.sep
        app_path = sep.join(request.path.strip(sep).split(sep)[:2])
        host = request.META.get("HTTP_HOST")
        app_path = host + sep + app_path + sep
        log.info("app_path: %s", app_path)
        close_code = "http://" + app_path + code + sep
        log.info("close_code_reverse: %s", close_code)
        try:
            d = Device.objects.get(close_code=close_code)
        except Exception:
            log.error("Device not found %s", close_code)
            raise Http404("Device `{}` not found".format(code))
        if d.status == "close":
            return HttpResponse(json.dumps({"msg": "Already closed"}))
        else:
            user = User.objects.get(username="remote")
            a = Action(device=d, user=user)
            a.action_start = now()
            a.save()
            log.info('CloseRemote: RPyC server thread status: {}'.format(RPYC_SERVER_THREAD.is_alive()))
            try:
                MTU_SERVER.service.close_window(d.uuid)
            except Exception:
                log.exception('Failed close remote action')
        log.info("Command: close remote %s", d.uuid)
        return HttpResponse(json.dumps({"msg": "ok"}))
