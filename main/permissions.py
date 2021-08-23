# from rest_framework.permissions import BasePermission
#
#
# class IsPostAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and request.user == obj.author


from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
