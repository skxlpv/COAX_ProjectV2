from django.db import transaction
from rest_framework import serializers
from rest_framework.decorators import permission_classes

from api.permissions import IsWriter
from .models import User, Articles, Categories


# class CategoriesSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Categories
#         fields = ('id', 'name')
#         read_only_fields = ('id',)


class ArticlesSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # category = CategoriesSerializer()

    class Meta:
        model = Articles
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author',)
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        author = validated_data.pop('author')
        category = validated_data.pop('category')
        validated_data['category_id'] = category.id
        validated_data['author_id'] = author.email
        return super(ArticlesSerializer, self).create(validated_data)

