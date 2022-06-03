from django.db import transaction
from requests import Response
from rest_framework import serializers
from rest_framework.fields import Field

from hospitals.models import Hospitals
from hospitals.serializers import HospitalSerializer
from users.serializers import AuthorSerializer
from .models import Articles, Categories

Field.default_error_messages = {
    'category': "No such category",
}


class CategoriesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('name',)


def validate_category(value):
    if value['id'] not in Categories.objects.all().values_list('id', flat=True):
        raise serializers.ValidationError('No such category')
    return value

# def validate_category(self, value):
#     try:
#         Categories.objects.get(id=value["id"])
#     except Exception as e:
#         raise serializers.ValidationError('No such category')
#     return value


class ArticlesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    category = CategoriesSerializer()

    class Meta:
        model = Articles
        # fields = '__all__'
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author', 'hospital')
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category_id'] = category['id']
        return super(ArticlesSerializer, self).create(validated_data)
