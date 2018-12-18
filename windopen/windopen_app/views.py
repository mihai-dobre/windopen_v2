# Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, Http404
from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Python
import os
import json
from datetime import datetime, timedelta
from calendar import monthrange
import time
import hashlib
import random

# Models
from .models import Device, Action, Profile, UserProfile, UnregisteredDevice, User
from .forms import UserForm, NewDeviceForm
from windopen_starter.log import logger_windopen as log
from rpyc_server import MTU_SERVER


def index(request):
    print("index: " + str(request.user))

    context = {"hello": "world"}
    return render(request, "windopen/index.html", context)


@login_required
def actions_details(request, uuid):
    if request.method != "GET":
        return HttpResponseNotAllowed()
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
        if not action.user.username in users:
            r = lambda: random.randint(0, 255)
            colors.append({"user": action.user.username, "color": "#%02X%02X%02X" % (r(), r(), r())})
            users.append(action.user.username)
    log.info("colors: %s", colors)
    context.update({"colors": colors})
    context.update({"device": str(uuid)})
    log.info("@@@@@@@@@@@@@: %s", context)
    return render(request, "windopen/actions_details.html", context=context)
        

def open_window_remote(request, code):
    if request.method != "GET":
        return HttpResponseNotAllowed()
        
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
        a.action_start = datetime.now()
        a.save()
        MTU_SERVER.service.open_window(d.uuid)
    log.info("Command: open remote %s", d.uuid)
    return HttpResponse(json.dumps({"msg": "ok"}))


def close_window_remote(request, code):
    if request.method != "GET":
        return HttpResponseNotAllowed()
        
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
        a.action_start = datetime.now()
        a.save()
        MTU_SERVER.service.close_window(d.uuid)
    log.info("Command: close remote %s", d.uuid)
    return HttpResponse(json.dumps({"msg": "ok"}))


@login_required
def open_window(request):
    if request.method == "GET":
        log.info("request: %s", request.GET.get("uuid"))
#         return HttpResponse(json.dumps({"msg":"ok"}))
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
                a.action_start = datetime.now()
                a.save()
                MTU_SERVER.service.open_window(uuid)
            log.info("Command: open window %s", uuid)
            log.info("MTU_SERVER: %s", dir(MTU_SERVER))
            log.info("MTU_SERVER: %s", dir(MTU_SERVER.service))
            return HttpResponse(json.dumps({"msg": "ok"}))
        except Exception as err:
            log.error("ERROR: %s", err)
            HttpResponse("error")
    raise Http404("Use GET for actions")


@login_required
def close_window(request):
    if request.method == "GET":
        log.info("request: %s", request.GET.get("uuid"))
#         return HttpResponse(json.dumps({"msg":"ok"}))
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
                a.action_start = datetime.now()
                a.save()
                MTU_SERVER.service.close_window(uuid)
            log.info("Command: close window %s", uuid)
            log.info("MTU_SERVER: %s", MTU_SERVER)
            return HttpResponse(json.dumps({"msg": "ok"}))
        except Exception as err:
            log.error("ERROR: %s", err)
            HttpResponse("error")
    raise Http404("Use GET for actions")


@login_required
def actions(request):
    if request.method == "GET":
        log.info("request: %s", request.GET)
        req_params = request.GET
        interval = req_params.get("interval", "week")
        uuid = req_params.get("uuid")
        if interval == "week":
            end_day = datetime.now()
            start_day = end_day + timedelta(days=-7)
        elif interval == "year":
            end_day = datetime.now()
            if monthrange(end_day.year, 2)[1] == 29 and end_day.month > 2:
                start_day = end_day + timedelta(days=-366)
            else:
                start_day = end_day + timedelta(days=-365)
        elif interval == "day":
            end_day = datetime.now()
            start_day = end_day + timedelta(days=-1)
        else:
            end_day = datetime.now()
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
        log.info("graph info: %s", response)
        return HttpResponse(json.dumps({"actions": response}))
    else:
        return HttpResponseNotAllowed("Use GET for displaying actions")

@login_required
def generate_open_code(request):
    log.info("request path: %s", request.path)
    if request.method == "GET":
        sep = os.path.sep
        app_path = request.path.strip(sep).split(sep)[0]
        host = request.META.get("HTTP_HOST")
        app_path = host + sep + app_path + sep
        time_salt = time.time()
        uuid = request.GET.get("uuid", "")
        if not uuid:
            return HttpResponse(json.dumps({"open_code": "invalid device uuid `{}`".format(uuid)}))
        open_code = hashlib.sha224("{}{}".format(uuid, time_salt)).hexdigest()
        device = Device.objects.get(uuid = uuid, user=request.user)
        device.open_code = "http://" + app_path + "open_remote" + sep + open_code + sep
        device.save()
        return HttpResponse(json.dumps({"open_code": device.open_code}))
    else:
        return HttpResponseNotAllowed("Use GET to generate open code for device")


@login_required
def generate_close_code(request):
    if request.method == "GET":
        sep = os.path.sep
        app_path = request.path.strip(sep).split(sep)[0]
        host = request.META.get("HTTP_HOST")
        app_path = host + sep + app_path + sep
        time_salt = time.time()
        uuid = request.GET.get("uuid", "")
        if not uuid:
            return HttpResponse(json.dumps({"close_code": "invalid device uuid `{}`".format(uuid)}))
        close_code = hashlib.sha224("{}{}".format(uuid, time_salt)).hexdigest()
        device = Device.objects.get(uuid = uuid, user=request.user)
        device.close_code = "http://" + app_path + "close_remote" + sep + close_code + sep
        device.save()
        return HttpResponse(json.dumps({"close_code": device.close_code}))
    else:
        return HttpResponseNotAllowed("Use GET to generate close code for device")


@login_required
def devices(request):
    if request.method != "GET":
        return HttpResponseNotAllowed("Use GET to display devices")
    devices = []
    context = RequestContext(request).flatten()
    print(type(context))
    try:
        devices = Device.objects.filter(user=request.user)
    except Exception as err:
        log.warning("No devices registered for user: %s | %s", request.user, err)
    context.update({"devices": devices})
    return render(request, "windopen/devices.html", context=context)


@login_required
def new_device(request):
    if request.method == "POST":
        form = NewDeviceForm(request.POST)
        if not form.is_valid():
            log.error(dir(form.errors))
            log.error(form.errors["new_device"].data)
            return HttpResponse(
                json.dumps({
                    "status": "error",
                    "msg": form.errors["new_device"][0] if "new_device" in form.errors else form.errors,
                }),
                content_type="application/json",
            )
        else:
            log.info("new_sn: %s", form.cleaned_data)
            new_sn = form.cleaned_data["new_device"]
            # check if the device is already registerd
            existing_device = Device.objects.filter(uuid=new_sn)
            if existing_device:
                log.info("Device `%s` is already registered to user `%s`", new_sn, existing_device[0].user.username)
                status = "error"
                msg = "Device is already registered"
                return HttpResponse(json.dumps({"status": status, "msg": msg}), content_type="application/json")
            # check if the device is connected to the rpyc server and if is in the unregistered table
            unreg_device = UnregisteredDevice.objects.filter(uuid=new_sn)
            if unreg_device:
                d = Device(user=request.user, 
                           uuid=new_sn,
                           registered=datetime.now(),
                           last_seen=datetime.now(),
                           active=True)
                d.save()
                unreg_device.delete()
                status = "success"
                msg = "Successfully registered new device"
                log.info("Registered new device `%s` to user `%s`", new_sn, request.user)
                for i in range(10):
                    try:
                        a = Action(device=d, user=request.user)
                        if i % 2 == 1:
                            a.status = "open"
                        else:
                            a.status = "close"
                        a.action_start = datetime.now()-timedelta(5)
                        a.action_end = datetime.now()-timedelta(5)
                        a.save()
                    except Exception as err:
                        log.error("err create action: %s", err)
                    time.sleep(2)    
        
                log.info("done creating actions")
            else:
                status = "error"
                msg = "The device is not connected. Please connect the device and check for the green LED"
                log.warning("Device `%s` is not connected.", new_sn)

            return HttpResponse(json.dumps({"status": status, "msg": msg}), content_type="application/json")
    else:
        form = NewDeviceForm()
    return render(request, "windopen/new_device.html", context={"form": form})

##################
#  API Examples  #
##################


def api_examples(request):
    context = {"title": "API Examples Page"}
    return render(request, "windopen/api_examples.html", context)


######################
# Registration Views #
######################

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponseRedirect("/windopen/login/")
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(
        request,
        "windopen/register.html",
        {"user_form": user_form, "registered": registered}
    )


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/windopen/devices")
            else:
                return HttpResponse("Your Django Windopen account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "windopen/login.html", {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/windopen/login/")

