from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User


class PasswordCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="password_collection")
    title = models.CharField(max_length=255)


class Password(models.Model):
    collection = models.ForeignKey(PasswordCollection, on_delete=models.CASCADE, related_name="password")
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)


class PasswordAccessToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    password = models.ForeignKey(Password, on_delete=models.CASCADE, related_name="access_token")
