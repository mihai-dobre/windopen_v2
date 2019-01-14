from django.urls import re_path, include
from django.contrib import admin
from windopen_app.views import index

urlpatterns = [
    re_path(r"^$", index, name="index"),
    re_path(r"^windopen/", include("windopen_app.urls")),
    re_path(r"^admin/", admin.site.urls),
]
