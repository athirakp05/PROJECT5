# Generated by Django 4.2.5 on 2023-11-15 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellereditprofile',
            name='seller',
        ),
    ]
