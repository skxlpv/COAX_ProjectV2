from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from api.permissions import IsWriter, HasArticleUpdate
from articles.models import Article
from articles.serializers import ArticlesSerializer


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

    create:
    Create article

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
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Article.objects.filter(hospital=self.request.user.hospital)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)
