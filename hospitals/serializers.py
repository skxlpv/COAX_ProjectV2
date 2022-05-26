from rest_framework import serializers

from hospitals.models import Hospitals


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospitals
        fields = '__all__'