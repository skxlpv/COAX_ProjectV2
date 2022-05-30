from django.db import transaction
from rest_framework import serializers, status
from rest_framework.fields import Field
from rest_framework.response import Response

from hospitals.serializers import HospitalSerializer
from .models import Articles, Categories

Field.default_error_messages = {
    'category': "No such category",
}


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ArticlesSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = CategoriesSerializer()

    class Meta:
        model = Articles
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author',)
        read_only_fields = ('id',)
        extra_kwargs = {"category": {"error_messages": {"required": "Give yourself a username"}}}

    @transaction.atomic
    def create(self, validated_data):
        author = validated_data.pop('author')
        category = validated_data.pop('category')
        try:
            category = Categories.objects.get(name=category["name"])
        except:
            # category = Categories.objects.create(**category)
            return super(ArticlesSerializer, self).fail('category')
        validated_data['category_id'] = category.id
        validated_data['author_id'] = author.email
        return super(ArticlesSerializer, self).create(validated_data)
