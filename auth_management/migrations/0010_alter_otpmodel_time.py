# Generated by Django 3.2.7 on 2021-10-02 07:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_management', '0009_alter_otpmodel_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 2, 13, 14, 6, 337179)),
        ),
    ]
