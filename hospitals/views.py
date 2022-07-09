from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from hospitals.models import City, Hospital, Department
from hospitals.serializers import HospitalSerializer, CitySerializer, DepartmentSerializer


class CitiesViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    """
    Cities
    """

    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, ]


class HospitalsViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    Hospitals
    """

    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]


class DepartmentsView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    Departments
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, ]
