from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


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


# sends the current user data to the FrontEnd
@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({
        # user data, that should be passed to the FrontEnd
        'email': user.email,
    })
