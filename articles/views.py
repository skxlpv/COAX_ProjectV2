from rest_framework import mixins, serializers, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsWriter, IsLeader, IsHelper, IsCommon, HasArticleUpdate  # all the available permissions
from articles.models import Article
from articles.serializers import ArticlesSerializer, EditArticleSerializer
from users.models import User


class AddArticleViewSet(mixins.CreateModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated & IsWriter,)
    serializer_class = ArticlesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, hospital=self.request.user.hospital)


class ArticlesViewSet(mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):

    serializer_class = ArticlesSerializer


    @permission_classes(IsAuthenticated)
    def get_queryset(self):
        # return Articles.objects.all()
        return Article.objects.filter(hospital=self.request.user.hospital)

    @permission_classes(IsAuthenticated & HasArticleUpdate)
    @action(methods=['DELETE'], detail=True, url_path='delete', url_name='delete')
    def delete(self, request, pk):
        article = Article.objects.get(id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes(IsAuthenticated & HasArticleUpdate)
    @action(methods=['PUT', 'PATCH'], detail=True, url_path='edit', url_name='edit')
    def edit(self, request, pk):
        # print(IsSameAuthor.message)
        article = Article.objects.get(id=pk)
        serializer = EditArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EditArticleViewSet(mixins.UpdateModelMixin,
#                          GenericViewSet):
#     permission_classes(IsAuthenticated & HasArticleUpdate, )
#     queryset = Article
#     serializer_class = EditArticleSerializer
