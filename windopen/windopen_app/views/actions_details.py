import random

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.template import RequestContext
from django.shortcuts import render

from windopen_app.models import Action
from windopen_starter.log import logger_windopen as log


class ActionDetails(View):
    @method_decorator(login_required)
    def get(self, request, uuid):
        context = RequestContext(request).flatten()
        try:
            actions = Action.objects.filter(device_id=uuid)
        except Exception as err:
            log.warning("No actions on device: %s", err)
            actions = []
        context.update({"actions": actions})
        colors = []
        users = []
        for action in actions:
            if action.user.username not in users:
                r = lambda: random.randint(0, 255)
                colors.append({"user": action.user.username, "color": "#%02X%02X%02X" % (r(), r(), r())})
                users.append(action.user.username)
        context.update({"colors": colors})
        context.update({"device": str(uuid)})
        return render(request, "windopen/actions_details.html", context=context)
