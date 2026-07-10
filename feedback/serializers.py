"""DRF serializers: the boundary between the ORM models and the JSON API."""
from rest_framework import serializers

from .models import Board, Comment, Post


class BoardSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "organization", "name", "slug", "is_public", "post_count", "created_at"]
        read_only_fields = ["slug", "created_at"]

    def validate_organization(self, organization):
        """You can only create a board inside an organization you belong to."""
        user = self.context["request"].user
        if not organization.members.filter(pk=user.pk).exists():
            raise serializers.ValidationError("You are not a member of this organization.")
        return organization


class PostSerializer(serializers.ModelSerializer):
    # These three come from annotations added in PostViewSet.get_queryset, so the
    # whole page is serialized without extra queries per post.
    vote_count = serializers.IntegerField(source="votes_total", read_only=True)
    comment_count = serializers.IntegerField(source="comments_total", read_only=True)
    has_voted = serializers.BooleanField(read_only=True)
    author_email = serializers.EmailField(source="author.email", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "board", "title", "body", "status",
            "vote_count", "comment_count", "has_voted", "author_email", "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def validate_board(self, board):
        """You can only post on a board you can see (public, or one of your org's)."""
        user = self.context["request"].user
        if not Board.objects.visible_to(user).filter(pk=board.pk).exists():
            raise serializers.ValidationError("This board does not exist.")
        return board

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

    def validate_post(self, post):
        """You can only comment on a post whose board you can see."""
        user = self.context["request"].user
        if not Board.objects.visible_to(user).filter(pk=post.board_id).exists():
            raise serializers.ValidationError("This post does not exist.")
        return post
