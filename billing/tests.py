"""Tests for the billing API."""
from django.contrib.auth import get_user_model
from django.test import TestCase
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
