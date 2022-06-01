from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLeader(BasePermission):
    message = "Sorry, you don't have Leader or Admin rights for adding a post."

    def has_permission(self, request, view):
        # # чи метод (PUT, POST, GET...) є дозволеним
        # if request.method in SAFE_METHODS:
        #     return True

        # витяг ролі чи, можливо, адмінки поточного користувача
        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        # перевірка чи користувач є лідером чи адміном
        if user_roles == 'LD':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsHelper(BasePermission):
    message = "Sorry, you don't have Helper or Admin rights for adding a post."

    def has_permission(self, request, view):
        # if request.method in SAFE_METHODS:
        #     return True

        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        if user_roles == 'HP':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsCommon(BasePermission):
    message = "Sorry, you don't have Common or Admin rights for adding a post."

    def has_permission(self, request, view):
        # if request.method in SAFE_METHODS:
        #     return True

        user_roles = request.user.role
        is_superuser = request.user.is_superuser

        if user_roles == 'CM':
            return bool(request.user)
        elif is_superuser:
            return bool(request.user)


class IsWriter(BasePermission):
    message = "Sorry, you aren't able to write posts."

    def has_permission(self, request, view):
        # if request.method in SAFE_METHODS:
        #     return True

        is_writer = request.user.is_writer

        if is_writer:
            return bool(request.user)


# для редагування постів, перевіряє чи це той самий автор редагує свій пост
class IsSameAuthor(BasePermission):
    message = "You're not the author of this post"

    def has_object_permission(self, request, obj, view):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user