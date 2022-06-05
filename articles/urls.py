from django.urls import path
from rest_framework.routers import SimpleRouter

from articles import views

router = SimpleRouter(trailing_slash=True)
router.register('article', views.ArticlesViewSet, basename='articles')
router.register('create', views.AddArticleViewSet, basename='createArticle')
# router.register('edit', views.EditArticleViewSet, basename='editArticle')
urlpatterns = [
    # path('add/', views.AddArticleViewSet.as_view({'post': 'create'}), name='add-articles'),
    # path('', views.ArticlesViewSet.as_view({'get': 'list'}), name='add-articles')
]+router.urls
