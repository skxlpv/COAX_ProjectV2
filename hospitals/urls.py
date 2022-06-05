from django.urls import path
from rest_framework.routers import SimpleRouter

from hospitals.views import CitiesListViewSet, HospitalsListViewSet, DepartmentsListView

router = SimpleRouter()
router.register('', HospitalsListViewSet, basename='hospitals')
# router.register('{pk}', HospitalsListViewSet, basename='hospital')

router.register('cities', CitiesListViewSet, basename='cities')
router.register('departments', DepartmentsListView, basename='departments')

urlpatterns = [
] + router.urls
