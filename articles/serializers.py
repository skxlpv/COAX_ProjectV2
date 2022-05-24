from django.db import transaction
from rest_framework import serializers

# from articles.models import Articles
from .models import User, Articles


class ArticleSerializer(serializers.ModelSerializer):
    # author = AuthorSerializer
    # email = User.objects.get(id=author.id)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Articles
        fields = ('id', 'status', 'title', 'excerpt', 'text',  'author')
        read_only_fields = ('id',)

    @transaction.atomic
    def create(self, validated_data):
        author = validated_data.pop('author')
        print(User.objects.get(id=author.id))
        validated_data['author_id'] = author.email
        return super(ArticleSerializer, self).create(validated_data)

