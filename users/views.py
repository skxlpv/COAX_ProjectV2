from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import api_view, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.permissions import IsSameUser
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer, EditPasswordSerializer, EditUserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(hospital=self.request.user.hospital)
    serializer_class = UserSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     GenericViewSet):

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    serializer_class = ProfileSerializer

    # serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSameUser)
    # queryset = User.objects.all()

    # @swagger_auto_schema(request_body=EditUserSerializer)
    @action(methods=['PATCH'], detail=False, serializer_class=EditUserSerializer, url_path='edit', url_name='edit')
    def edit(self, request):
        instance = self.request.user
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)

    # @swagger_auto_schema(request_body=EditPasswordSerializer)
    @action(methods=['PATCH'], detail=False, serializer_class=EditPasswordSerializer, url_path='change-password', url_name='change-password')
    def change_password(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({'email': user.email})
