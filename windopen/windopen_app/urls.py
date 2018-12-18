from django.conf.urls import re_path, url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"^register/$", views.register, name="register"),
    url(r"^login/$", views.user_login, name="login"),
    url(r"^logout/$", views.user_logout, name="logout"),
    url(r"^api/$", views.api_examples, name="api"),
    url(r"^devices/$", views.devices, name="devices"),
    url(r"^new_device/$", views.new_device, name="new_device"),
    url(r"^actions/$", views.actions, name="actions"),
    url(r"^actions_details/(?P<uuid>[^/]+)/$", views.actions_details, name="actions_details"),
    url(r"^open_code/$", views.generate_open_code, name="open_code"),
    url(r"^close_code/$", views.generate_close_code, name="close_code"),
    url(r"^open_window/$", views.open_window, name="open_window"),
    url(r"^close_window/$", views.close_window, name="close_window"),
    url(r"^open_remote/(?P<code>[^/]+)/$", views.open_window_remote, name="open_window_remote"),
    url(r"^close_remote/(?P<code>[^/]+)/$", views.close_window_remote, name="close_window_remote"),
    ]
