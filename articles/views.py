from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

# from api.permissions import IsLeader
from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon
from articles.models import Articles
from articles.serializers import ArticleSerializer


class AddArticleViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    permission_classes = (IsAuthenticated, IsWriter, IsCommon)
    # queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

class ArticlesViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    # queryset = Articles.objects.filter(status='review')       # Відображає лиш ті, які потребують підтвердження
    # queryset = Articles.objects.filter(status='published')   # Відображає лиш підтверджені
    queryset = Articles.objects.all()
    # Відображає всі
    serializer_class = ArticleSerializer
