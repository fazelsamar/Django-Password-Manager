from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from django.core import exceptions as django_exceptions
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
            raise serializers.ValidationError(
                {"err": "Can't create user"}
            )
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    otp = serializers.IntegerField(required=False)
