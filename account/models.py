from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.DateTimeField()

    @classmethod
    def get_user_token(cls, user, ip_address):
        """
        Get or create token for user and its ip address
        """
        token, _ = Token.objects.get_or_create(
            user=user,
            token=make_password(ip_address, salt=getattr(settings, 'TOKEN_SALT', "asdf"))
        )
        expiration_seconds = getattr(settings, 'TOKEN_EXPIRATION_SECONDS', 3600)
        token.expired = timezone.now() + timezone.timedelta(seconds=expiration_seconds)
        token.save()
        return token
