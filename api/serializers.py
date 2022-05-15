from rest_framework import serializers
from base.models import Post
from users.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')

class RegisterUserSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'password')
        # extra_kwargs = {'password': {'write-only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
