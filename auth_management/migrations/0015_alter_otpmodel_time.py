# Generated by Django 3.2.7 on 2021-10-02 08:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_management', '0014_alter_otpmodel_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 2, 14, 29, 4, 208963)),
        ),
    ]