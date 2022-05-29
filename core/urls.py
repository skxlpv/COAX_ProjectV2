from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('v1/', include('api.urls')),
    path('v1/user/', include('users.urls', namespace='users')),
    path('v1-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('admin/', admin.site.urls),
    path('', include('base.urls'), name='base'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('articles/', include('articles.urls'), name='articles'),
    path('hospitals/', include('hospitals.urls'), name='hospitals'),
    path('management/', include('management.urls'), name='management'),
]

