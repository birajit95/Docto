# Generated by Django 3.2.7 on 2021-10-03 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0010_alter_doctordetails_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='doctor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_details', to=settings.AUTH_USER_MODEL),
        ),
    ]
