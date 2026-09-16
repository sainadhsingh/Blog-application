from rest_framework.routers import DefaultRouter
from .api import PostViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='api-posts')
router.register(r'categories', CategoryViewSet, basename='api-categories')
router.register(r'tags', TagViewSet, basename='api-tags')

urlpatterns = router.urls
