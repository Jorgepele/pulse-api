"""Feedback domain: boards, feature-request posts, votes and comments."""
from django.conf import settings
from django.db import models
from django.utils.text import slugify

from accounts.models import Organization


class Board(models.Model):
    """A collection of feature requests, owned by an organization."""

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="boards"
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("organization", "slug")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.organization})"


class Post(models.Model):
    """A single feature request / feedback item on a board."""

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        DONE = "done", "Done"
        DECLINED = "declined", "Declined"

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def vote_count(self) -> int:
        return self.votes.count()

    def __str__(self):
        return self.title


class Vote(models.Model):
    """An upvote from a user on a post. One vote per user per post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user} → {self.post}"


class Comment(models.Model):
    """A comment thread entry on a post."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
