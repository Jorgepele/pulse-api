"""Billing views: the public plan list plus a (demo) subscribe endpoint.

Billing here is *simulated*: subscribing records a Subscription in the database
but no real payment is taken. It gives the product a complete SaaS flow without
depending on a Stripe account. A real Stripe integration would replace the body
of SubscriptionView.post with a Checkout session.
"""
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """Plans are public so the landing page can render pricing without a login."""

    queryset = Plan.objects.order_by("price_cents")
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]


class SubscriptionView(APIView):
    """Read or change the current organization's subscription (demo, no payment)."""

    permission_classes = [IsAuthenticated]

    def _organization(self, request):
        # A user subscribes on behalf of their (first) organization.
        return request.user.organizations.first()

    def get(self, request):
        org = self._organization(request)
        sub = Subscription.objects.filter(organization=org).first() if org else None
        return Response(SubscriptionSerializer(sub).data if sub else None)

    def post(self, request):
        org = self._organization(request)
        if org is None:
            return Response(
                {"detail": "You need an organization to subscribe."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        plan = get_object_or_404(Plan, slug=request.data.get("plan"))
        sub, _ = Subscription.objects.update_or_create(
            organization=org,
            defaults={"plan": plan, "status": Subscription.Status.TRIALING},
        )
        return Response(SubscriptionSerializer(sub).data)
