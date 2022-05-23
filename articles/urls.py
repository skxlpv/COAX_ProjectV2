from django.urls import path

from articles import views

urlpatterns = [
    path('', views.ArticleVieSet.as_view({'get': 'list', 'post': 'create'}), name='articles-list')
]
