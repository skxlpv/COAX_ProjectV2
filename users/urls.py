from rest_framework.routers import SimpleRouter

from .views import UsersViewSet

router = SimpleRouter(trailing_slash=True)
router.register('', UsersViewSet, basename='users-list')

app_name = 'users'

urlpatterns = [
] + router.urls
