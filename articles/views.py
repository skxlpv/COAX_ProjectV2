from rest_framework import mixins, serializers, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from articles import serializers as ser
from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, HasArticleUpdate  # all the available permissions
from articles.models import Article
from articles.serializers import ArticlesSerializer, EditArticleSerializer

# @action(methods=['PUT', 'PATCH'], detail=True, url_path='edit', url_name='edit')

class ArticlesViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):
    """
    list:
    Get list of articles

    ## Get detailed information about articles

    URLs
    ```python
    All articles:
    GET http://127.0.0.1:8000/v1/articles/

    Specific article:
    GET http://127.0.0.1:8000/v1/articles/x
    ```

    create:
    Create article

    URL
    ```python
    POST http://127.0.0.1:8000/v1/articles/
    ```

    Request example
    ```python
    {
      "title": "string",
      "excerpt": "string",
      "text": "string",
      "category_id": int
    }
    ```

    """

    permission_classes = (IsAuthenticated, HasArticleUpdate, IsWriter)

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update',):
            return ser.EditArticleSerializer
        return ser.ArticlesSerializer

    def get_queryset(self):
        # return Article.objects.all()
        return Article.objects.filter(hospital=self.request.user.hospital)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)

