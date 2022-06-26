from rest_framework import serializers

from hospitals.serializers import HospitalSerializer
from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    hospital = HospitalSerializer(many=False, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'hospital', 'doctor', 'check_in_date', 'diagnosis', 'receipt']

    def update(self, patient, validated_data):
        diagnosis = self.validated_data.get('diagnosis')
        if not diagnosis:
            raise serializers.ValidationError('No diagnosis was given')

        receipt = self.validated_data.get('receipt')
        if not receipt:
            raise serializers.ValidationError('No receipt was given')

        patient.receipt = validated_data['receipt']
        patient.diagnosis = validated_data['diagnosis']
        patient.save()
        return patient
