from django.urls import path
from rest_framework.routers import SimpleRouter

from hospitals.views import CitiesViewSet, HospitalsViewSet, DepartmentsView

router = SimpleRouter()
router.register(r'', HospitalsViewSet, basename='hospital-list')
router.register(r'city', CitiesViewSet, basename='city-list')
router.register(r'department', DepartmentsView, basename='department-list')

urlpatterns = [

] + router.urls
