from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from hospitals.models import City, Hospital, Department
from hospitals.serializers import HospitalSerializer, CitySerializer, DepartmentSerializer


class CitiesListViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, ]


class HospitalsListViewSet(mixins.ListModelMixin,
                           GenericViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]


class DepartmentsListView(mixins.ListModelMixin,
                          GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, ]
