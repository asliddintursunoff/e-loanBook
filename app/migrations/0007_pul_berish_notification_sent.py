# Generated by Django 5.2.1 on 2025-06-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_customuser_can_show_harajatlar'),
    ]

    operations = [
        migrations.AddField(
            model_name='pul_berish',
            name='notification_sent',
            field=models.BooleanField(default=False),
        ),
    ]
