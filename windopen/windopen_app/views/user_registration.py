from django.views import View
from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ValidationError

from windopen_starter.log import logger_windopen as log
from windopen_app.forms import UserForm


class RegisterUser(View):

    def get(self, request):
        user_form = UserForm()

        return render(
            request,
            "windopen/register.html",
            {"user_form": user_form, "registered": False}
        )

    def post(self, request):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return HttpResponseRedirect("/windopen/login/")
        else:
            log.error(user_form.error)
            # TODO:
            # gather the form errors and propagate them to upper levels -> template
            raise ValidationError("Registration form validation failed")
            # return HttpResponseRedirect("/windopen/register/")
