# Generated by Django 5.2.1 on 2025-06-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_pul_olish_status_pul_olish_tolangan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pul_olish',
            name='sabab',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='pul_olish',
            name='tolangan',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30),
        ),
    ]
