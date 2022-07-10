from rest_framework.permissions import BasePermission


class IsLeader(BasePermission):
    message = "Sorry, you don't have Leader or Admin rights for adding a post."

    def has_permission(self, request, view):
        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        if user_roles == 'LD':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsHelper(BasePermission):
    message = "Sorry, you don't have Helper or Admin rights for adding a post."

    def has_permission(self, request, view):
        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        if user_roles == 'HP':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsCommon(BasePermission):
    message = "Sorry, you don't have Common or Admin rights for adding a post."

    def has_permission(self, request, view):
        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        if user_roles == 'CM':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsWriter(BasePermission):
    message = "Sorry, you aren't able to write posts."

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_writer
        return True


class IsSameUser(BasePermission):
    message = "You're not this user"

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH',):

            if obj == request.user:
                return True
            return False

        return True


class HasArticleUpdate(BasePermission):
    message = "You're not the author of this post"

    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            if obj.author == request.user:
                return True
            return False

        return True


class HasEventDestroy(BasePermission):
    message = "You're not the creator of this event"

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.creator == request.user:
                return True
            return False
        return True
