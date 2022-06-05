from django.urls import path

from hospitals.views import CitiesListViewSet, HospitalsListViewSet, DepartmentsListView

urlpatterns = [
    path('', CitiesListViewSet.as_view({'get': 'list'}), name='cities'),
    path('hospitals/', HospitalsListViewSet.as_view({'get': 'list'}), name='hospitals'),
    path('hospitals/departments', DepartmentsListView.as_view({'get': 'list'}), name='hospitals'),
    # path('new-hospital/', CitiesViewSet.as_view({'post': 'create'}), name='hospital'),
]
