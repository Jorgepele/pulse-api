"""Billing views: the public plan list, a (demo) subscribe endpoint, and an
optional real Stripe Checkout flow.

By default billing is *simulated*: SubscriptionView records a Subscription in
the database but takes no real payment, so the demo has a complete SaaS flow
without a Stripe account. When STRIPE_SECRET_KEY is configured, CheckoutView
starts a real Stripe Checkout session (test mode) and StripeWebhookView
activates the subscription once payment completes. See billing/BILLING.md.
"""
from django.conf import settings
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


class CheckoutView(APIView):
    """Start a real Stripe Checkout session for a plan (test mode).

    Only available when STRIPE_SECRET_KEY is set; otherwise the demo uses the
    simulated SubscriptionView instead.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not settings.STRIPE_ENABLED:
            return Response(
                {"detail": "Stripe is not configured; use the demo subscribe endpoint."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )

        org = request.user.organizations.first()
        if org is None:
            return Response(
                {"detail": "You need an organization to subscribe."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        plan = get_object_or_404(Plan, slug=request.data.get("plan"))
        if not plan.stripe_price_id:
            return Response(
                {"detail": "This plan has no Stripe price configured."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        import stripe

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
            client_reference_id=str(org.id),
            metadata={"organization_id": str(org.id), "plan_id": str(plan.id)},
        )
        return Response({"checkout_url": session.url})


class StripeWebhookView(APIView):
    """Receive Stripe events. Activates the subscription on checkout completion.

    Stripe calls this endpoint directly, so it takes no user auth; instead the
    payload signature is verified against STRIPE_WEBHOOK_SECRET.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        import stripe

        try:
            event = stripe.Webhook.construct_event(
                request.body,
                request.META.get("HTTP_STRIPE_SIGNATURE", ""),
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            meta = session.get("metadata") or {}
            org_id, plan_id = meta.get("organization_id"), meta.get("plan_id")
            if org_id and plan_id:
                Subscription.objects.update_or_create(
                    organization_id=org_id,
                    defaults={
                        "plan_id": plan_id,
                        "status": Subscription.Status.ACTIVE,
                        "stripe_customer_id": session.get("customer") or "",
                        "stripe_subscription_id": session.get("subscription") or "",
                    },
                )
        return Response(status=status.HTTP_200_OK)
