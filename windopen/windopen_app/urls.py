from django.conf.urls import url

from windopen_app.views import *

urlpatterns = [
    url(r"^register/$", RegisterUser.as_view(), name="register"),
    url(r"^login/$", user_login, name="login"),
    url(r"^logout/$", user_logout, name="logout"),
    url(r"^devices/$", Devices.as_view(), name="devices"),
    url(r"^new_device/$", RegisterDevice.as_view(), name="new_device"),
    url(r"^actions/$", Actions.as_view(), name="actions"),
    url(r"^actions_details/(?P<uuid>[^/]+)/$", ActionDetails.as_view(), name="actions_details"),
    url(r"^open_code/$", GenOpenCode.as_view(), name="open_code"),
    url(r"^close_code/$", GenCloseCode.as_view(), name="close_code"),
    url(r"^open_window/$", OpenWindow.as_view(), name="open_window"),
    url(r"^close_window/$", CloseWindow.as_view(), name="close_window"),
    url(r"^open_remote/(?P<code>[^/]+)/$", OpenWindowRemote.as_view(), name="open_window_remote"),
    url(r"^close_remote/(?P<code>[^/]+)/$", CloseWindowRemote.as_view(), name="close_window_remote"),
    ]
