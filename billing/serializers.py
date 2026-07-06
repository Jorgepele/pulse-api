"""Serializer for subscription plans (the public pricing table)."""
from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "slug", "price_cents", "max_boards"]
