from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, IsSameAuthor  # all the available permissions
from articles.models import Articles
from articles.serializers import ArticleSerializer


class AddArticleViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated, IsWriter)
    # queryset = Articles.objects.all()
    serializer_class = ArticleSerializer


class ArticlesViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    # permission_classes = (IsAuthenticated,)
    # queryset = Articles.objects.filter(status='review')       # Shows only that, which need confirmation
    # queryset = Articles.objects.filter(status='published')    # Shows only confirmed
    queryset = Articles.objects.all()                           # Shows all
    serializer_class = ArticleSerializer
