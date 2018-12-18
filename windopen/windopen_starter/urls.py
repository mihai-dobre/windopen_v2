from django.urls import path, re_path, include
from django.contrib import admin
from windopen_app import views

urlpatterns = [
    # path(""),
    re_path(r"^$", views.index, name="index"),
    re_path(r"^windopen/", include("windopen_app.urls")),
    re_path(r"^admin/", admin.site.urls),
    # url(r"^openid/(.*)", SessionConsumer()),
]
