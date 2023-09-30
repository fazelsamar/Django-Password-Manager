from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

from .models import Token


class CustomTokenAuthentication(BaseAuthentication):
    keyword = "Bearer"
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _("Invalid token header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid token header. Token string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _(
                "Invalid token header. Token string should not contain invalid characters."
            )
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.model
        try:
            token = model.objects.get(token=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        if token.expired <= timezone.now():
            raise exceptions.AuthenticationFailed(_("Expired Token."))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("User inactive or deleted."))

        return token.user, None

    def authenticate_header(self, request):
        return self.keyword
