from datetime import datetime

from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from patients.models import Patient
from patients.serializers import PatientSerializer


class PatientViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     GenericViewSet):

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user,
                        hospital=self.request.user.hospital,
                        check_in_date=datetime.utcnow())

    queryset = Patient.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = PatientSerializer