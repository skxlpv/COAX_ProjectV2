from django.urls import path

from hospitals.views import HospitalViewSet

urlpatterns = [
    path('new-hospital/', HospitalViewSet.as_view({'post':'create'}), name='hospital'),
]