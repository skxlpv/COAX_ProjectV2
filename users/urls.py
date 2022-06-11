from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import BlackListTokenView, current_user, UsersViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

router = SimpleRouter()
router.register('', UsersViewSet, basename='users')

urlpatterns = [
    path('logout/blacklist/', BlackListTokenView.as_view(), name='blacklist'),
    path('user/', current_user, name='user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
