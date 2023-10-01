from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from django.core import exceptions as django_exceptions
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings

from . import models

User = get_user_model()


class PasswordCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PasswordCollection
        fields = ["id", "user", "title"]
        read_only_fields = ["user", "id"]

    def create(self, validated_data):
        return models.PasswordCollection.objects.create(user=self.context['user'], **validated_data)


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Password
        fields = ["id", "collection", "name", "username", "password"]
        read_only_fields = ["id", "collection"]

    def create(self, validated_data):
        return models.Password.objects.create(collection_id=self.context['collection_id'], **validated_data)
