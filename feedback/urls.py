from rest_framework.routers import DefaultRouter

from .views import BoardViewSet, CommentViewSet, PostViewSet

router = DefaultRouter()
router.register("boards", BoardViewSet)
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
