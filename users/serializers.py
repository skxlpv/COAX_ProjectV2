from rest_framework import serializers
import django.contrib.auth.password_validation as validators

from .models import User


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
    class Meta:
        model = User
        fields = ['id', 'image', 'first_name', 'last_name', 'email']
        read_only_fields = fields
