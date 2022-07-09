from rest_framework import serializers
from hospitals.models import City, Hospital, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city', 'region')
        read_only_fields = ('id', )


class HospitalSerializer(serializers.ModelSerializer):
    region = CitySerializer(many=False, read_only=True)
    hospital_departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = ('id', 'name', 'region', 'hospital_departments')
        read_only_fields = ('id', 'hospital_departments')
