from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BlackListTokenView, current_user, UserViewSet, ProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = SimpleRouter(trailing_slash=True)
router.register(r'', UserViewSet, basename='users-list')
router.register(r'my-profile', ProfileViewSet, basename='my-profile')

app_name = 'users'

urlpatterns = [
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist'),

    # path('user/', current_user, name='user'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
