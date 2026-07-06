"""Billing views: the public list of plans (the pricing table)."""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Plan
from .serializers import PlanSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Plans are public so the landing page can render pricing without a login."""

    queryset = Plan.objects.order_by("price_cents")
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]
