from rest_framework import serializers
from hospitals.models import City, Hospital, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'department_name')
        read_only_fields = ('id', )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city', 'region')
        read_only_fields = ('id', )


class HospitalSerializer(serializers.ModelSerializer):
    region = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Hospital
        fields = ('id', 'hospital_name', 'region')
        read_only_fields = ('id', )
