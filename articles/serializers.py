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
    id = serializers.IntegerField()

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('name',)


class EditArticleSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'excerpt', 'text', 'category', 'status')
        read_only_fields = ('id',)

    def validate_category(self, value):
        try:
            Category.objects.get(id=value["id"])
        except Exception as e:
            raise serializers.ValidationError('No such category')
        return value

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)
        instance.text = validated_data.get('text', instance.text)
        instance.status = validated_data.get('status', instance.status)
        instance.category = Category.objects.get(id=validated_data['category']['id'])
        instance.save()
        return instance


class ArticlesSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    hospital = HospitalSerializer(read_only=True)
    category = CategoriesSerializer()

    class Meta:
        model = Article
        fields = ('id', 'status', 'title', 'excerpt', 'text', 'category', 'author', 'hospital')
        read_only_fields = ('id',)

    def validate_category(self, value):
        try:
            Category.objects.get(id=value["id"])
        except Exception as e:
            raise serializers.ValidationError('No such category')
        return value

    @transaction.atomic
    def create(self, validated_data):
        category = validated_data.pop('category')
        validated_data['category_id'] = category['id']
        return super(ArticlesSerializer, self).create(validated_data)
