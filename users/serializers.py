from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'hospital', 'role', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


