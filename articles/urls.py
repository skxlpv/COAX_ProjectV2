from django.urls import path

from articles import views

urlpatterns = [
    path('add/', views.AddArticleViewSet.as_view({'post': 'create'}), name='add-articles'),
    path('', views.ArticlesViewSet.as_view({'get': 'list'}), name='add-articles')
]
