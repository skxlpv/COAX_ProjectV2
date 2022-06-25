from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import current_user, UserViewSet, ProfileViewSet, ProfileListViewSet

router = SimpleRouter(trailing_slash=False)
router.register(r'', UserViewSet, basename='users-list')
router.register(r'profiles/', ProfileListViewSet, basename='profile-list')

app_name = 'users'

urlpatterns = [
    path('my-profile/', ProfileViewSet.as_view({'get':'list'}), name='my-profile'),
] + router.urls
