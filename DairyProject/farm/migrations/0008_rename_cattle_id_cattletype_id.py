# Generated by Django 4.2.5 on 2023-11-01 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0007_cattletype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cattletype',
            old_name='cattle_id',
            new_name='id',
        ),
    ]