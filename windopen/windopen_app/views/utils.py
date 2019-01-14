from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def index(request):

    context = {"hello": "world"}
    return render(request, "windopen/index.html", context)


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
            # print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "windopen/login.html", {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/windopen/login/")
