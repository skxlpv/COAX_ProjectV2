from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'created_at', 'diagnosis', 'receipt', 'doctor']

    def validate_diagnosis(self, value):
        if value is None:
            raise ValidationError('No diagnosis was provided')
        return value

    def validate_receipt(self, value):
        if value is None:
            raise ValidationError('No receipt was provided')
        return value

    def update(self, instance, validated_data):
        # other way updating it updates only one field, while the other becomes null
        instance.receipt = validated_data.get('receipt', instance.receipt)
        instance.diagnosis = validated_data.get('diagnosis', instance.diagnosis)
        instance.save()
        return instance
