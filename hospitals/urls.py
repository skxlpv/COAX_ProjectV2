from django.urls import path
from rest_framework.routers import SimpleRouter

from hospitals.views import CitiesViewSet, HospitalsViewSet, DepartmentsView

router = SimpleRouter()
router.register('hospital', HospitalsViewSet, basename='hospital-list')
router.register('city', CitiesViewSet, basename='city-list')
router.register('department', DepartmentsView, basename='department-list')

urlpatterns = [

] + router.urls
