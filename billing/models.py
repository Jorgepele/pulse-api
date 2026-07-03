"""Billing domain: subscription plans and per-organization subscriptions (Stripe test mode)."""
from django.db import models

from accounts.models import Organization


class Plan(models.Model):
    """A subscription tier. Prices stored in cents to avoid float rounding."""

    name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=60, unique=True)
    price_cents = models.PositiveIntegerField(default=0)
    max_boards = models.PositiveIntegerField(default=1)
    stripe_price_id = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.name} (${self.price_cents / 100:.2f})"


class Subscription(models.Model):
    """Links an organization to the plan it is currently paying for."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        TRIALING = "trialing", "Trialing"
        PAST_DUE = "past_due", "Past due"
        CANCELED = "canceled", "Canceled"

    organization = models.OneToOneField(
        Organization, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.TRIALING
    )
    stripe_customer_id = models.CharField(max_length=120, blank=True)
    stripe_subscription_id = models.CharField(max_length=120, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization} → {self.plan} [{self.status}]"
