from rest_framework import serializers
from rest_framework import status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsSameUser
from users.models import User
from users.serializers import ProfileSerializer, EditPasswordSerializer, EditUserSerializer


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(hospital=self.request.user.hospital)
    serializer_class = ProfileSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     # mixins.UpdateModelMixin,
                     GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsSameUser)

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

    def get_object(self):
        return self.request.user

    # def perform_update(self, serializer):
    #     instance = self.get_object()
    #     return serializer.save()
    # @swagger_auto_schema(request_body=EditUserSerializer)
    @action(methods=['PATCH'], detail=False, serializer_class=EditUserSerializer, url_path='edit', url_name='edit')
    def edit(self, request):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    # @swagger_auto_schema(request_body=EditPasswordSerializer)
    @action(methods=['PUT'], detail=False, serializer_class=EditPasswordSerializer, url_path='change-password',
            url_name='change-password')
    def change_password(self, request):
        user = self.get_object()
        serializer = self.serializer_class(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)
