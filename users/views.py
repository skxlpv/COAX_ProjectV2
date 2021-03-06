from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsSameUser
from users.models import User
from users.serializers import ProfileSerializer, EditPasswordSerializer, EditUserSerializer


class UsersViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    """
    list:
    List of profiles

    ### Get all the profiles from current hospital

    read:
    Single profile

    ### Get detailed information about user by {id}.
    #### You should belong to the hospital, where this user is

    """

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(hospital=self.request.user.hospital)

    serializer_class = ProfileSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    """
    list:
    My profile

    ### Get the profile of the current user

    partial_update:
    Change user data

    ### Email must be unique
    ### Validations in serializer:
    * Default email validation
    * Parsing to lower and checking in DB


    change_password:
    Change password

    ### Password validation:

    ```python
    validators.validate_password()
    ```

    * Not common
    * Not only numeric
    * 8 or more symbols
    """

    permission_classes = (IsAuthenticated, IsSameUser)

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return EditUserSerializer
        elif self.request.method == 'PUT':
            return EditPasswordSerializer
        return ProfileSerializer

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(request_body=EditUserSerializer)
    def partial_update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=EditPasswordSerializer)
    def change_password(self, request):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)
