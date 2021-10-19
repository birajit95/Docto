from django.db import models
from user_management.models import User


class AppointmentPlan(models.Model):
    name = models.CharField(max_length=100)
    valid_days = models.IntegerField(default=7)
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    discount_percent = models.FloatField(default=0.0)
    actual_price = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.price


class DoctorTimings(models.Model):
    day_choices = (
        ('SUNDAY', 'SUNDAY'),
        ('MONDAY', 'MONDAY'),
        ('TUESDAY', 'TUESDAY'),
        ('WEDNESDAY', 'WEDNESDAY'),
        ('THURSDAY', 'THURSDAY'),
        ('FRIDAY', 'FRIDAY'),
        ('SATURDAY', 'SATURDAY'),

    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='doctor_for_timings'
    )
    day = models.CharField(max_length=20, choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_busy = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)


class Appointment(models.Model):
    appointment_mode_choices = (
        ("online", "online"),
        ("offline", "offline")
    )

    consultation_status_choices = (
        ("running", "running"),
        ("completed", "completed"),
        ("pending", "pending"),
    )

    appointment_status_choices = (
        ("instant", "instant"),
        ("incoming", "incoming")
    )

    appointment_id = models.CharField(max_length=300)
    appointment_plan = models.ForeignKey(
        AppointmentPlan, on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='doctor')
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='patient')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_status = models.CharField(choices=appointment_status_choices, default="instant", max_length=10)
    appointment_mode = models.CharField(choices=appointment_mode_choices, default='online', max_length=10)
    consultation_status = models.CharField(choices=consultation_status_choices, default='pending', max_length=15)
    is_cancelled = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
