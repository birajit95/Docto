from django.contrib.auth.models import AbstractUser
from django.db import models
from master_management.models import Address, Doctor_Type


class User(AbstractUser):
    country_code = models.CharField(max_length=4)
    mobile = models.CharField(max_length=20)
    dob = models.DateField(null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        ordering = ['-date_joined']


class DoctorDetails(models.Model):
    doctor = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_details',
    )
    specialization = models.ForeignKey(
        Doctor_Type, on_delete=models.CASCADE
    )
    qualifications = models.JSONField()
    practice_start_date = models.DateField()
    registration_number = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True
    )

