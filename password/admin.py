from django.contrib import admin

from . import models

admin.site.register(models.PasswordCollection)
admin.site.register(models.Password)
admin.site.register(models.PasswordAccessToken)
