from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import current_user, UserViewSet, ProfileViewSet, ProfileListViewSet

router = SimpleRouter(trailing_slash=True)
# router.register(r'', UserViewSet, basename='users-list')
router.register(r'', ProfileListViewSet, basename='profile-list')
router.register(r'my-profile', ProfileViewSet, basename='profile')

app_name = 'users'

urlpatterns = [
] + router.urls
