from rest_framework.permissions import BasePermission
from users.models import User


class IsOwnerOrReadOnly(BasePermission):
    message = "Sorry, you should be the owner of this article." \
              "Please try another one."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user