from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import Field

from hospitals.serializers import HospitalSerializer
from users.serializers import AuthorSerializer
from .models import Article, Category


Field.default_error_messages = {
    'category': "No such category",
}


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id', 'name',)


class ArticlesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Article
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'category_id', 'author', 'hospital')
        read_only_fields = ('id',)
