from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PlanViewSet, SubscriptionView

# SimpleRouter (not DefaultRouter) so it doesn't add a second "api-root" name,
# which would clash with the feedback router mounted at the same prefix.
router = SimpleRouter()
router.register("plans", PlanViewSet)

urlpatterns = router.urls + [
    path("billing/subscription/", SubscriptionView.as_view(), name="subscription"),
]
