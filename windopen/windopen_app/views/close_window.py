import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.timezone import now
from django.http import HttpResponse, HttpResponseBadRequest, Http404

from windopen_app.models import Device, Action
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER, RPYC_SERVER_THREAD


class CloseWindow(View):

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
            if d.status == "close":
                return HttpResponse(json.dumps({"msg": "Already closed"}))
            else:
                a = Action(device=d, user=request.user)
                a.action_start = now()
                a.save()
                log.info('CloseWindow: RPyC server thread status: {}'.format(RPYC_SERVER_THREAD.is_alive()))
                try:
                    MTU_SERVER.service.close_window(uuid)
                except Exception:
                    log.exception('Failed close action')
            log.info("Command: close window %s", uuid)
            return HttpResponse(json.dumps({"msg": "ok"}))
        except Exception as err:
            log.exception("ERROR: %s", err)
            HttpResponse(json.dumps({"msg": "error"}))
