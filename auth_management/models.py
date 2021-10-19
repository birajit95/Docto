from django.db import models
from django.contrib.auth.models import Group
from user_management.models import User
from datetime import datetime


class Module(models.Model):
    name = models.CharField(max_length=50)
    list = models.BooleanField(default=False)
    retrieve = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    update = models.BooleanField(default=False)
    destroy = models.BooleanField(default=False)
    profile_1 = models.BooleanField(default=False)
    profile_2 = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    role = models.ForeignKey(
        Group, on_delete=models.PROTECT
    )
    module = models.ForeignKey(
        Module, on_delete=models.PROTECT
    )
    allowed_permissions = models.JSONField()

    def __str__(self):
        return self.role.name + " on " + self.module.name


class OTPModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT
    )
    otp = models.CharField(max_length=20)
    time = models.DateTimeField(default=datetime.now())
    is_verified = models.BooleanField(default=False)
    reset_token = models.CharField(max_length=300, null=True, blank=True)
