from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from hospitals.serializers import HospitalSerializer
from .models import User, Profile


class EditUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no changes',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


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
