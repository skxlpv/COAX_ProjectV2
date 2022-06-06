from rest_framework import mixins, serializers, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, HasArticleUpdate  # all the available permissions
from articles.models import Articles, Categories
from articles.serializers import ArticlesSerializer, EditArticleSerializer
from users.models import User


# class AddArticleViewSet(mixins.CreateModelMixin,
#                         GenericViewSet):
#     permission_classes = (IsAuthenticated & IsWriter)
#     serializer_class = ArticlesSerializer
#
#


class ArticlesViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.CreateModelMixin,
                      GenericViewSet):

    serializer_class = ArticlesSerializer
    permission_classes = (IsAuthenticated, HasArticleUpdate, IsWriter)

    def get_queryset(self):
        return Articles.objects.all()
        # return Articles.objects.filter(hospital=self.request.user.hospital)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)

    def perform_update(self, serializer):
        category = Categories.objects.get(id=self.request.data['category']['id'])
        serializer.save(category=category)

