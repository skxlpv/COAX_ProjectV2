from rest_framework import serializers

from hospitals.models import Hospital
from hospitals.serializers import HospitalSerializer
from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(many=False, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'hospital', 'doctor', 'check_in_date', 'diagnosis', 'receipt']
