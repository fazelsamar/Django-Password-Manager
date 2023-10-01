from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from .permissions import IsPasswordCollectionOwner

User = get_user_model()


class PasswordCollectionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PasswordCollectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.PasswordCollection.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'user': self.request.user}


class PasswordViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PasswordSerializer
    permission_classes = [IsAuthenticated, IsPasswordCollectionOwner]

    def get_queryset(self):
        return models.Password.objects.filter(
            collection_id=self.kwargs['collection_pk'],
            collection__user=self.request.user
        ).select_related("collection", "collection__user")

    def get_serializer_context(self):
        return {'collection_id': self.kwargs['collection_pk']}
