# Generated by Django 4.2.5 on 2023-11-05 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_alter_cattle_health_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cattle',
            name='has_insurance',
            field=models.BooleanField(default=False, help_text='Check if the cattle has insurance'),
        ),
        migrations.AddField(
            model_name='cattle',
            name='has_vaccination',
            field=models.BooleanField(default=False, help_text='Check if the cattle has vaccination'),
        ),
    ]
