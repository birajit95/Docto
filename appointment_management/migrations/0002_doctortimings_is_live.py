# Generated by Django 3.2.7 on 2021-10-03 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctortimings',
            name='is_live',
            field=models.BooleanField(default=False),
        ),
    ]
