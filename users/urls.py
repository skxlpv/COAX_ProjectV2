from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, ProfileViewSet

router = SimpleRouter(trailing_slash=True)
router.register('', UsersViewSet, basename='users-list')
router.register(r'my-profile', ProfileViewSet, basename='profile')

app_name = 'users'

urlpatterns = [
    path(r'my-profile/', ProfileViewSet.as_view({'get':'list'}), name='profile')
] + router.urls
