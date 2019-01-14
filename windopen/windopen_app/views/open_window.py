import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseBadRequest, Http404

from windopen_app.models import Device, Action
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER


class OpenWindow(View):

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        log.info("request: %s", request.GET.get("uuid"))
        try:
            uuid = request.GET.get("uuid", "")
            if not uuid:
                return HttpResponseBadRequest("Empty uuid")
            try:
                d = Device.objects.get(uuid=uuid)
            except Exception as err:
                d = None
            log.info("a luat device: %s", d.__dict__)
            if not d:
                raise Http404("Device `{}` not found".format(uuid))
            if d.status == "open":
                return HttpResponse(json.dumps({"msg": "Already opened"}))
            else:
                a = Action(device=d, user=request.user)
                a.action_start = now()
                a.save()
                MTU_SERVER.service.open_window(uuid)
            log.info("Command: open window %s", uuid)
            log.info("MTU_SERVER: %s", dir(MTU_SERVER))
            log.info("MTU_SERVER: %s", dir(MTU_SERVER.service))
            return HttpResponse(json.dumps({"msg": "ok"}))
        except Exception as err:
            log.error("ERROR: %s", err)
            HttpResponse("error")
