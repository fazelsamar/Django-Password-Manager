import random

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()


class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expired = models.DateTimeField()

    otp = models.PositiveSmallIntegerField(null=True, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_user_token(cls, user, ip_address):
        """
        Get or create token for user and its ip address
        """
        token, _ = Token.objects.get_or_create(
            user=user,
            token=make_password(ip_address, salt=getattr(settings, 'TOKEN_SALT', "asdf"))
        )
        return token

    def extend_token_and_invalid_otp(self):
        expiration_seconds = getattr(settings, 'TOKEN_EXPIRATION_SECONDS', 3600)
        self.expired = timezone.now() + timezone.timedelta(seconds=expiration_seconds)
        self.otp = random.randint(111111, 999999)
        self.otp_expired = None
        self.save()
        return self

    def set_otp(self):
        if self.otp_expired and self.otp_expired >= timezone.now():
            return "Otp already sent"
        random.seed()
        self.otp = random.randint(111111, 999999)
        expiration_seconds = getattr(settings, 'OTP_EXPIRATION_SECONDS', 60)
        self.otp_expired = timezone.now() + timezone.timedelta(seconds=expiration_seconds)
        self.save()
        # TODO: Send Email
        return "New Otp sent"

    def check_otp(self, otp_code):
        if self.otp == otp_code and self.otp_expired <= timezone.now():
            return True
        return False
