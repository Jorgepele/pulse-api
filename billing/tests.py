"""Tests for the billing API."""
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from accounts.models import Membership, Organization
from .models import Plan, Subscription

User = get_user_model()


class PlanAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Plan.objects.create(name="Free", slug="free", price_cents=0, max_boards=1)
        Plan.objects.create(name="Pro", slug="pro", price_cents=1900, max_boards=10)

    def test_plans_are_public(self):
        response = self.client.get("/api/plans/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_plans_ordered_by_price(self):
        response = self.client.get("/api/plans/")
        names = [p["name"] for p in response.data["results"]]
        self.assertEqual(names, ["Free", "Pro"])


class SubscriptionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.plan = Plan.objects.create(name="Pro", slug="pro", price_cents=1900, max_boards=10)
        self.user = User.objects.create_user(email="s@example.com", password="pw12345!")
        self.org = Organization.objects.create(name="Acme", owner=self.user)
        Membership.objects.create(user=self.user, organization=self.org)

    def test_subscribe_creates_subscription(self):
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/billing/subscription/", {"plan": "pro"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["plan_name"], "Pro")
        self.assertEqual(response.data["status"], "trialing")
        self.assertEqual(Subscription.objects.count(), 1)

    def test_subscribe_is_idempotent_per_org(self):
        self.client.force_authenticate(self.user)
        self.client.post("/api/billing/subscription/", {"plan": "pro"})
        self.client.post("/api/billing/subscription/", {"plan": "pro"})
        self.assertEqual(Subscription.objects.count(), 1)

    def test_get_subscription_returns_current(self):
        self.client.force_authenticate(self.user)
        self.client.post("/api/billing/subscription/", {"plan": "pro"})
        response = self.client.get("/api/billing/subscription/")
        self.assertEqual(response.data["plan_name"], "Pro")

    def test_subscribe_requires_authentication(self):
        response = self.client.post("/api/billing/subscription/", {"plan": "pro"})
        self.assertIn(response.status_code, (401, 403))


@override_settings(
    STRIPE_ENABLED=True,
    STRIPE_SECRET_KEY="sk_test_dummy",
    STRIPE_WEBHOOK_SECRET="whsec_dummy",
)
class StripeCheckoutTests(TestCase):
    """The real-Stripe path, with the Stripe SDK mocked (no network)."""

    def setUp(self):
        self.client = APIClient()
        self.plan = Plan.objects.create(
            name="Pro", slug="pro", price_cents=1900, max_boards=10,
            stripe_price_id="price_test_123",
        )
        self.user = User.objects.create_user(email="pay@example.com", password="pw12345!")
        self.org = Organization.objects.create(name="Acme", owner=self.user)
        Membership.objects.create(user=self.user, organization=self.org)

    @mock.patch("stripe.checkout.Session.create")
    def test_checkout_returns_a_stripe_url(self, create):
        create.return_value = mock.Mock(url="https://checkout.stripe.test/abc")
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/billing/checkout/", {"plan": "pro"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["checkout_url"], "https://checkout.stripe.test/abc")
        # The session carries the org + plan so the webhook can activate it.
        _, kwargs = create.call_args
        self.assertEqual(kwargs["metadata"]["organization_id"], str(self.org.id))
        self.assertEqual(kwargs["line_items"][0]["price"], "price_test_123")

    def test_webhook_activates_the_subscription(self):
        event = {
            "type": "checkout.session.completed",
            "data": {"object": {
                "metadata": {"organization_id": str(self.org.id), "plan_id": str(self.plan.id)},
                "customer": "cus_test",
                "subscription": "sub_test",
            }},
        }
        with mock.patch("stripe.Webhook.construct_event", return_value=event):
            response = self.client.post(
                "/api/billing/webhook/", data="{}", content_type="application/json",
                HTTP_STRIPE_SIGNATURE="t=1,v1=x",
            )
        self.assertEqual(response.status_code, 200)
        sub = Subscription.objects.get(organization=self.org)
        self.assertEqual(sub.status, "active")
        self.assertEqual(sub.stripe_subscription_id, "sub_test")


@override_settings(STRIPE_ENABLED=False, STRIPE_SECRET_KEY="")
class StripeDisabledTests(TestCase):
    def test_checkout_is_unavailable_without_a_key(self):
        client = APIClient()
        user = User.objects.create_user(email="no@example.com", password="pw12345!")
        org = Organization.objects.create(name="Acme", owner=user)
        Membership.objects.create(user=user, organization=org)
        client.force_authenticate(user)
        response = client.post("/api/billing/checkout/", {"plan": "pro"})
        self.assertEqual(response.status_code, 501)
