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
    id = serializers.IntegerField()

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('name',)


class EditArticleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Articles
        fields = ('id', 'title', 'excerpt', 'text', 'category', 'status')
        read_only_fields = ('id',)

    def validate_category(self, value):
        try:
            Categories.objects.get(id=value["id"])
        except Exception as e:
            raise serializers.ValidationError('No such category')
        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)
        instance.text = validated_data.get('text', instance.text)
        instance.status = validated_data.get('status', instance.status)
        instance.category = Categories.objects.get(id=validated_data['category']['id'])
        instance.save()
        return instance


class ArticlesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    hospital_name = HospitalSerializer(many=False, read_only=False)
    category = CategoriesSerializer()

    class Meta:
        model = Articles
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author', 'hospital_name')
        read_only_fields = ('id', 'hospital_name')

    def validate_category(self, value):
        try:
            Categories.objects.get(id=value["id"])
        except Exception as e:
            raise serializers.ValidationError('No such category')
        return value

    @transaction.atomic
    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category_id'] = category['id']
        return super(ArticlesSerializer, self).create(validated_data)
