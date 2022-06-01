from rest_framework import serializers
from hospitals.models import Hospitals


class HospitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospitals
        fields = ('id', 'name', 'region')
        read_only_fields = ('id',)
