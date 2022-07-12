from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from api.permissions import HasPatientDestroy, HasPatientUpdate
from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    """
     list:
     List of patients

     ### Here user gets list of his own patients from hospital, where they belong

     create:
     Patient

     ### Create new patient, required first_name, last_name and an email. Doctor and hospital are taken automaticaly

     read:
     Single patient

     ### Get detailed information about specific patient by {id}.
     #### You should belong to the hospital, where this patient is

     update:
     Patient

     ### Diagnosis and receipt can be updated

     partial_update:
     Patient

     ### Diagnosis and receipt can be updated

     delete:
     Patient

     ### Delete patient

     """

    permission_classes = (IsAuthenticated, HasPatientDestroy, HasPatientUpdate)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user, hospital=self.request.user.hospital)

    def get_queryset(self):
        queryset = Patient.objects.all().filter(hospital=self.request.user.hospital)
        doctor = self.request.query_params.get('doctor')
        if doctor is not None:
            queryset = queryset.filter(doctor__first_name__startswith=doctor) | \
                       queryset.filter(doctor__last_name__startswith=doctor)
        return queryset
