from django.db import transaction
from rest_framework import serializers

# from articles.models import Articles
from .models import User, Articles


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer

    class Meta:
        model = Articles
        fields = ('id', 'category', 'title', 'excerpt', 'text', 'author')
        read_only_fields = ('id', )

    @transaction.atomic
    def create(self, validated_data):
        author = validated_data.pop('author')
        # author = User.objects.create(**author)
        # validated_data['author_hospital'] = author.hospital
        validated_data['author_id'] = author.id

        print(validated_data)
        return super(ArticleSerializer, self).create(validated_data)

