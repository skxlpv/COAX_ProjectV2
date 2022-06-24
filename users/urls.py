from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import current_user, UserViewSet, ProfileViewSet

router = SimpleRouter(trailing_slash=True)
router.register(r'', UserViewSet, basename='users-list')
router.register(r'my-profile', ProfileViewSet, basename='my-profile')

app_name = 'users'

urlpatterns = [
    # path('user/', current_user, name='user'),
] + router.urls
