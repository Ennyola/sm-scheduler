from django.contrib import admin
from django.urls import path, include

from scheduler.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path(
        "manage-accounts/",
        include("social_media_integration.urls", namespace="social_integration"),
    ),
]
