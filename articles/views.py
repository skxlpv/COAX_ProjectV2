from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from api.permissions import IsWriter, HasArticleUpdate
from articles.models import Article
from articles.serializers import ArticlesSerializer, ArticleViewSerializer, ArticleEditViewSerializer


@method_decorator(name='create', decorator=swagger_auto_schema(
    request_body=ArticleViewSerializer, responses={200: ArticlesSerializer(many=True)}
))
@method_decorator(namArticlee='update', decorator=swagger_auto_schema(
    request_body=ArticleEditViewSerializer, responses={200: ArticlesSerializer(many=True)}
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    request_body=ArticleEditViewSerializer, responses={200: ArticlesSerializer(many=True)}
))
class ArticlesViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):
    """
    list:
    Get list of articles

    ### Here user get list of articles from hospital, where user belong

    create:
    Create article

    ### Create new article, by giving text, excerpt, text and category. Author and hospital will be taken automatically
    # User must have permission "isWriter"

    read:
    Get article

    ### Get detailed information about specific article by {id}.
    #### You should belong to the hospital, where this article is

    update:
    Update article

    ### User must be original author of article

    partial_update:
    Partially update article

    ### User must be original author of article

    delete:
    Delete article

    ### Delete article, if user is the author of article

    """

    permission_classes = (IsAuthenticated, HasArticleUpdate, IsWriter)
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Article.objects.filter(hospital=self.request.user.hospital)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)
