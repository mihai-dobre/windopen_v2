from django.urls import re_path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from windopen_app.views import index

urlpatterns = [
    re_path(r"^$", index, name="index"),
    re_path(r"^windopen/", include("windopen_app.urls")),
    re_path(r"^admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
