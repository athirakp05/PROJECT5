# Generated by Django 4.2.5 on 2023-11-07 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0010_alter_cattle_farmer_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cattle',
            name='farmer_license',
            field=models.CharField(max_length=7, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(message='Seller license must be in the format FXXXXX, where X is a digit (0-9).', regex='^F\\d{5}$')]),
        ),
    ]
