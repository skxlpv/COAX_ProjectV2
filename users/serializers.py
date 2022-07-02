from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from rest_framework import serializers, status
from rest_framework.response import Response
import django.contrib.auth.password_validation as validators
from rest_framework.validators import UniqueValidator

from .models import User, Profile


class EditPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
    )

    class Meta:
        model = User
        fields = ['id', 'password']

    def validate(self, data):
        validators.validate_password(password=data['password'])
        return data


class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("User already exist")
        return value.lower()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'hospital', 'role', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', )
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']
        read_only_fields = fields
