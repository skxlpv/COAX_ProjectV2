from django.urls import path
# from .views import PostList, PostDetail
#
# app_name = 'api'
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import BlackListTokenView

urlpatterns = [
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]