# Generated by Django 4.2.5 on 2024-03-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='society',
            name='location',
        ),
        migrations.AddField(
            model_name='society',
            name='pin_code',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
