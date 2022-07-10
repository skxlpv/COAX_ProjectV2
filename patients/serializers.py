from rest_framework import serializers

from patients.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'created_at', 'diagnosis', 'receipt', 'doctor', 'is_discharged']

    def update(self, instance, validated_data):
        instance.receipt = validated_data.get('receipt', instance.receipt)
        instance.diagnosis = validated_data.get('diagnosis', instance.diagnosis)
        instance.is_discharged = validated_data.get('is_discharged', instance.is_discharged)
        instance.save()
        return instance
