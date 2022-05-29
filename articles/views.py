from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, IsSameAuthor  # усі доступні кастомні дозволи
from articles.models import Articles
from articles.serializers import ArticlesSerializer


class AddArticleViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated & IsWriter,)
    serializer_class = ArticlesSerializer


class ArticlesViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    # queryset = Articles.objects.filter(status='review')       # Відображає лиш ті, які потребують підтвердження
    # queryset = Articles.objects.filter(status='published')   # Відображає лиш підтверджені
    queryset = Articles.objects.all()                          # Відображає всі
    serializer_class = ArticlesSerializer
