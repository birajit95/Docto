# Generated by Django 3.2.7 on 2021-10-17 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointment_management', '0002_doctortimings_is_live'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_id', models.CharField(max_length=300)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('appointment_status', models.CharField(choices=[('instant', 'instant'), ('incoming', 'incoming')], default='instant', max_length=10)),
                ('appointment_mode', models.CharField(choices=[('online', 'online'), ('offline', 'offline')], default='online', max_length=10)),
                ('consultation_status', models.CharField(choices=[('running', 'running'), ('completed', 'completed'), ('pending', 'pending')], default='pending', max_length=15)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
