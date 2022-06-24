from django.contrib.auth.hashers import make_password
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
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):

    # def get_queryset(self):
    #     return Profile.objects.filter(user=self.request.user)
    # serializer_class = ProfileSerializer

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update',):
            return EditUserSerializer
        return UserSerializer
    permission_classes = (IsAuthenticated, IsSameUser)
    queryset = User.objects.all()

    @action(methods=['PATCH'], detail=False, serializer_class=EditPasswordSerializer, url_path='change-password', url_name='change-password')
    def change_password(self, request):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({'email': user.email})
