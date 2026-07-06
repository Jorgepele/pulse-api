"""Seed a small, realistic demo dataset so the API (and the React frontend) has
something to show: one organization, a public board and a handful of posts.

Run it with:  python manage.py seed_demo

It is idempotent — running it twice won't create duplicates, so it's safe to
re-run while developing.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from accounts.models import Membership, Organization
from billing.models import Plan
from feedback.models import Board, Post

User = get_user_model()

DEMO_EMAIL = "demo@pulse.dev"
DEMO_PASSWORD = "demo12345"

# The pricing tiers shown on the landing page. (name, slug, price_cents, max_boards)
PLANS = [
    ("Free", "free", 0, 1),
    ("Pro", "pro", 1900, 10),
]

# Example feature requests, as a real feedback board might collect them.
POSTS = [
    ("Dark mode", "A theme toggle so the dashboard is easier on the eyes at night."),
    ("Slack notifications", "Notify a channel whenever a post reaches 50 votes."),
    ("Export to CSV", "Let admins download all feedback for a board as a CSV file."),
    ("Mobile app", "A companion app to browse and vote on the go."),
]


class Command(BaseCommand):
    help = "Create a demo user, organization, board and example posts."

    def handle(self, *args, **options):
        # get_or_create keeps the command idempotent. We (re)set the password on
        # every run so the demo credentials are always known, even if the user
        # already existed from an earlier session.
        user, _ = User.objects.get_or_create(
            email=DEMO_EMAIL, defaults={"full_name": "Demo User"}
        )
        user.set_password(DEMO_PASSWORD)
        user.save()

        org, _ = Organization.objects.get_or_create(
            slug="demo", defaults={"name": "Demo Co.", "owner": user}
        )
        Membership.objects.get_or_create(
            user=user, organization=org, defaults={"role": Membership.Role.OWNER}
        )

        board, _ = Board.objects.get_or_create(
            organization=org, slug="feature-requests",
            defaults={"name": "Feature requests", "is_public": True},
        )

        for name, slug, price_cents, max_boards in PLANS:
            Plan.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "price_cents": price_cents, "max_boards": max_boards},
            )

        for title, body in POSTS:
            Post.objects.get_or_create(
                board=board, title=title, defaults={"body": body, "author": user}
            )

        self.stdout.write(self.style.SUCCESS(
            f"Seeded '{org.name}' with board '{board.name}' "
            f"and {board.posts.count()} posts. "
            f"Login: {DEMO_EMAIL} / {DEMO_PASSWORD}"
        ))
