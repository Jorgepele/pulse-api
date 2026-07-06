"""Tests for the billing API."""
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Plan


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
