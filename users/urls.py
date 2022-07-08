from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet, ProfileViewSet

router = SimpleRouter(trailing_slash=True)
router.register('', UsersViewSet, basename='users-list')

app_name = 'users'

urlpatterns = [
    path(r'my-profile/', ProfileViewSet.as_view({'get': 'list', "patch": "partial_update"}),
         name='profile'),
    path(r'my-profile/change-password', ProfileViewSet.as_view({"put": "change_password"}),
         name='profile-change-password')
] + router.urls
