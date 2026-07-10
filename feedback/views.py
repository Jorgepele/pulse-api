"""API views (the 'controller' layer): boards, posts and the vote toggle action."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Board, Comment, Post, Vote
from .serializers import BoardSerializer, CommentSerializer, PostSerializer


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.visible_to(self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.select_related("author", "board").filter(
            board__in=Board.objects.visible_to(self.request.user)
        )
        board = self.request.query_params.get("board")
        if board:
            qs = qs.filter(board_id=board)
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """Toggle the current user's upvote on this post."""
        post = self.get_object()
        vote, created = Vote.objects.get_or_create(post=post, user=request.user)
        if not created:
            vote.delete()
        return Response({"voted": created, "vote_count": post.vote_count})


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.select_related("author").filter(
            post__board__in=Board.objects.visible_to(self.request.user)
        )
        post = self.request.query_params.get("post")
        if post:
            qs = qs.filter(post_id=post)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
