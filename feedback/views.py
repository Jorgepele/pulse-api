"""API views (the 'controller' layer): boards, posts and the vote toggle action."""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Board, Comment, Post, Vote
from .serializers import BoardSerializer, CommentSerializer, PostSerializer


class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        qs = Post.objects.select_related("author", "board")
        board = self.request.query_params.get("board")
        if board:
            qs = qs.filter(board_id=board)
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
        qs = Comment.objects.select_related("author")
        post = self.request.query_params.get("post")
        if post:
            qs = qs.filter(post_id=post)
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
