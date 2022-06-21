from rest_framework import status, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer


class BlackListTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({'email': user.email})
