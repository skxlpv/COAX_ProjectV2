from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from hospitals.models import City, Hospital, Department
from hospitals.serializers import HospitalSerializer, CitySerializer, DepartmentSerializer


class CitiesViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    GenericViewSet):
    """
    list:
    List of cities

    ### Here user gets a list of all cities, that can be filtered by URL

    read:
    City

    ### Get detailed information about specific city by {id}.

    """

    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = City.objects.all()
        city = self.request.query_params.get('city')

        # if there is "/city/?city=some_city" in url
        if city is not None:
            queryset = queryset.filter(city__istartswith=city)
        return queryset


class HospitalsViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       GenericViewSet):
    """
    list:
    List of hospitals

    ### Here user gets a list of all hospitals, that can be filtered by URL

    read:
    Hospital

    ### Get detailed information about specific hospital by {id}.

    """

    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = Hospital.objects.all()
        hospital = self.request.query_params.get('name')

        # if there is "/hospitals/?hospital=some_city" in url
        if hospital is not None:
            queryset = queryset.filter(name__istartswith=hospital)
        return queryset


class DepartmentsView(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    list:
    List of departments

    ### Here user gets a list of all departments,
    that are present in current hospital and can be filtered by URL

    read:
    Department

    ### Get detailed information about specific department by {id}.

    """

    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        queryset = Department.objects.all()
        department = self.request.query_params.get('name')

        # if there is "/department/?name=some_dep" in url
        if department is not None:
            queryset = queryset.filter(name__istartswith=department)
        return queryset
