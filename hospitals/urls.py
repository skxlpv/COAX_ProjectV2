from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter

from hospitals.views import CitiesViewSet, HospitalsViewSet, DepartmentsView

router = DefaultRouter(trailing_slash=True)
router.register(r'department', DepartmentsView, basename='department')
router.register(r'city', CitiesViewSet, basename='city')
router.register(r'', HospitalsViewSet, basename='hospital')

urlpatterns = [

] + router.urls
