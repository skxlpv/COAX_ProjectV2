from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

    def get_queryset(self):
        queryset = Patient.objects.all()
        doctor = self.request.query_params.get('doctor') # get doctor

        # if there is "/?doctor=somename&somelastname" in url,
        # search all patients by their doctor's name and lastname
        if doctor is not None:
            queryset = queryset.filter(doctor__first_name__startswith=doctor) | \
                       queryset.filter(doctor__last_name__startswith=doctor)
        return queryset
