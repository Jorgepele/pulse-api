from django.contrib import admin

from .models import Board, Comment, Post, Vote


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "is_public", "created_at")
    list_filter = ("is_public",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "status", "vote_count", "created_at")
    list_filter = ("status", "board")
    search_fields = ("title", "body")


admin.site.register(Vote)
admin.site.register(Comment)
