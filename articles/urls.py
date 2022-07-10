from rest_framework.routers import SimpleRouter

from articles import views

router = SimpleRouter(trailing_slash=True)
router.register(r'', views.ArticlesViewSet, basename='articles')

urlpatterns = [
]+router.urls
