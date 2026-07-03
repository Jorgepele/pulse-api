"""Root URL configuration for the Pulse API."""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_request):
    return JsonResponse({"status": "ok", "service": "pulse-api"})


urlpatterns = [
    path("", health, name="health"),
    path("admin/", admin.site.urls),
    path("api/", include("feedback.urls")),
    path("api-auth/", include("rest_framework.urls")),  # browsable-API login
]
