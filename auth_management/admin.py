from django.contrib import admin
from .models import Module, Permission, OTPModel

admin.site.register(Module)
admin.site.register(Permission)
admin.site.register(OTPModel)

