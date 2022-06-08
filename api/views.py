# from rest_framework import generics
# from rest_framework.permissions import BasePermission, DjangoModelPermissions, SAFE_METHODS
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from articles.models import Article
# from .serializers import ArticleSerializer
#
#
# class TheOnlyAuthorPermission(BasePermission):
#     message = 'Only the author of the post can edit it.'
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.author == request.user
#
#
# class PostList(generics.ListCreateAPIView):
#     permission_classes = [DjangoModelPermissions]
#     queryset = Article.postobjects.all()
#     serializer_class = ArticleSerializer
#
#
# class PostDetail(generics.RetrieveDestroyAPIView, TheOnlyAuthorPermission):
#     permission_classes = [TheOnlyAuthorPermission]
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
