from rest_framework.routers import DefaultRouter

from management.views import ItemViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')
router.register(r'categories', CategoryViewSet, basename='categories')
urlpatterns = router.urls
