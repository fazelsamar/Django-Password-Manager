from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

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

    @action(permission_classes=[IsAuthenticated], detail=True)
    def get_password_access_token(self, request, *args, **kwargs):
        password = get_object_or_404(models.Password, pk=kwargs.get("pk"))
        if password.collection.user != request.user:
            return Response(
                {"msg": "The user does not the owner of password"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        password_token, _ = models.PasswordAccessToken.objects.get_or_create(
            password=password
        )
        return Response(
            {"password_token_id": password_token.id},
            status=status.HTTP_200_OK,
        )


class GetPasswordByToken(views.APIView):
    def get(self, request, token_id, *args, **kwargs):
        password_token = get_object_or_404(models.PasswordAccessToken, pk=token_id)
        return Response({
            "name": password_token.password.name,
            "username": password_token.password.username,
            "password": password_token.password.password,
        }, status=status.HTTP_200_OK)
