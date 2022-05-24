from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from articles.models import Articles
from articles.serializers import ArticleSerializer


class ArticleVieSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    # queryset = Articles.objects.filter(status='review')       # Відображає лиш ті, які потребують підтвердження
    # queryset = Articles.objects.filter(status='published')   # Відображає лиш підтверджені
    queryset = Articles.objects.all()
    # Відображає всі
    serializer_class = ArticleSerializer
