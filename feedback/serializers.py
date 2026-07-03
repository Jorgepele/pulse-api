"""DRF serializers: the boundary between the ORM models and the JSON API."""
from rest_framework import serializers

from .models import Board, Comment, Post


class BoardSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "organization", "name", "slug", "is_public", "post_count", "created_at"]
        read_only_fields = ["slug", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    vote_count = serializers.IntegerField(read_only=True)
    author_email = serializers.EmailField(source="author.email", read_only=True)
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "board", "title", "body", "status",
            "vote_count", "has_voted", "author_email", "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def get_has_voted(self, post) -> bool:
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return post.votes.filter(user=request.user).exists()

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "body", "author_email", "created_at"]
        read_only_fields = ["created_at"]
