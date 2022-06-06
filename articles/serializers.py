from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import Field

from hospitals.serializers import HospitalSerializer
from users.serializers import AuthorSerializer
from .models import Articles, Categories


Field.default_error_messages = {
    'category': "No such category",
}


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id', 'name',)


class EditArticleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all().values_list('id', flat=True),
        write_only=True
    )

    class Meta:
        model = Articles
        fields = ('id', 'title', 'excerpt', 'text', 'category', 'category_id', 'status')
        read_only_fields = ('id',)


class ArticlesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all().values_list('id', flat=True),
        write_only=True
    )

    class Meta:
        model = Articles
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'category_id', 'author', 'hospital')
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        validated_data['category_id'] = validated_data.pop('category_id')
        return super(ArticlesSerializer, self).create(validated_data)
