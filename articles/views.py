from django.views.decorators.http import require_GET, require_http_methods
from rest_framework import mixins, serializers, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, IsSameAuthor  # all the available permissions
from articles.models import Articles
from articles.serializers import ArticlesSerializer
from users.models import User


class AddArticleViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated & IsWriter,)
    serializer_class = ArticlesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)


class ArticlesViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticlesSerializer

    def get_queryset(self):
        return Articles.objects.filter(hospital=self.request.user.hospital)
