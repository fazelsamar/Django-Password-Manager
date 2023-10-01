import random

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.core.mail import send_mail


class Token(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15)
    expired = models.DateTimeField(default="2000-01-01")

    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_expired = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "ip_address",)

    @classmethod
    def get_user_token(cls, user, ip_address):
        """
        Get or create token for user and its ip address
        """
        token_str = str(ip_address) + str(user.username)
        token, _ = Token.objects.get_or_create(
            user=user,
            ip_address=ip_address,
            token=make_password(token_str, salt=getattr(settings, 'TOKEN_SALT', "asdf"))
        )
        return token

    def extend_token_and_invalid_otp(self):
        expiration_seconds = getattr(settings, 'TOKEN_EXPIRATION_SECONDS', 3600)
        self.expired = timezone.now() + timezone.timedelta(seconds=expiration_seconds)
        self.otp = None
        self.otp_expired = None
        self.save()
        return self

    def sent_otp(self):
        if self.otp_expired and self.otp_expired >= timezone.now():
            return "Otp already sent"
        random.seed()
        self.otp = random.randint(111111, 999999)
        expiration_seconds = getattr(settings, 'OTP_EXPIRATION_SECONDS', 60)
        self.otp_expired = timezone.now() + timezone.timedelta(seconds=expiration_seconds)
        self.save()
        # Send Email
        send_mail(
            "Login To Password Manager",
            f"The opt code is {self.otp}, you have {expiration_seconds} seconds.",
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False
        )
        return "New Otp sent"

    def check_otp(self, otp_code):
        if not self.otp or self.otp != otp_code:
            return "Invalid otp"
        if not self.otp_expired or self.otp_expired <= timezone.now():
            return "Otp is expired"
        return False
