from rest_framework.routers import SimpleRouter

from events.views import EventViewSet

router = SimpleRouter()
router.register('', EventViewSet, basename='events-list')

urlpatterns = [

] + router.urls
