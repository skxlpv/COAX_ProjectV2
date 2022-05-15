from rest_framework import serializers
from base.models import Post
from django.contrib.auth.password_validation import validate_password
from base.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'password2', "first_name")

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        if CustomUser.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError(
                {"username": "User with this username already exists."})

        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError(
                {"email": "User with this email already exists."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop("password2", None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
