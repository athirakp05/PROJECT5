# Generated by Django 4.2.5 on 2024-02-21 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0023_rename_description_appointment_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.TextField(default=True),
        ),
    ]
