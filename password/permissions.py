from rest_framework import permissions
from django.shortcuts import get_object_or_404

from .models import PasswordCollection


class IsPasswordCollectionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.collection.user == request.user

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve the collection object based on the URL parameter
            collection_pk = view.kwargs.get('collection_pk')
            collection = get_object_or_404(PasswordCollection, pk=collection_pk)

            # Check if the user is the owner of the collection
            if collection.user == request.user:
                return True

        return False
