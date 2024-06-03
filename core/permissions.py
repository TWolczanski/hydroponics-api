from rest_framework import permissions


class IsHydroponicSystemOwner(permissions.BasePermission):
    message = "You cannot access other users' hydroponic systems."

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
