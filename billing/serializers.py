"""Serializers for the billing API: plans and subscriptions."""
from rest_framework import serializers

from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "slug", "price_cents", "max_boards"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "plan", "plan_name", "status", "current_period_end", "created_at"]
        read_only_fields = ["status", "current_period_end", "created_at"]
