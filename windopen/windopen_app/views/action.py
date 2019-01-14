import json
from calendar import monthrange

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from django.utils.timezone import now, timedelta

from windopen_app.models import Action
from windopen_starter.log import logger_windopen as log


class Action(View):
    @method_decorator(login_required)
    def get(self, request):
        log.info("request: %s", request.GET)
        req_params = request.GET
        interval = req_params.get("interval", "week")
        uuid = req_params.get("uuid")
        end_day = now()
        if interval == "week":
            start_day = end_day + timedelta(days=-7)
        elif interval == "year":
            if monthrange(end_day.year, 2)[1] == 29 and end_day.month > 2:
                start_day = end_day + timedelta(days=-366)
            else:
                start_day = end_day + timedelta(days=-365)
        elif interval == "day":
            start_day = end_day + timedelta(days=-1)
        else:
            no_days = monthrange(end_day.year, end_day.month-1)[1]
            start_day = end_day + timedelta(days=no_days*-1)
        actions = Action.objects.filter(
            action_start__range=[start_day, end_day],
            device_id=uuid,
            status__in=["open", "close"]
        )
        response = []
        for action in actions:
            point = {"x": action.action_start.strftime("%Y,%m,%d,%H,%M,%S")}
            if action.status == "open":
                point["y"] = 1
            else:
                point["y"] = 0
            response.append(point)
        return HttpResponse(json.dumps({"actions": response}))
