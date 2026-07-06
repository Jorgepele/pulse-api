"""Root URL configuration for the Pulse API."""
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health(_request):
    return JsonResponse({"status": "ok", "service": "pulse-api"})


urlpatterns = [
    path("", health, name="health"),
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/", include("feedback.urls")),
    path("api/", include("billing.urls")),
    # OpenAPI schema and interactive docs (Swagger UI).
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api-auth/", include("rest_framework.urls")),  # browsable-API login
]
