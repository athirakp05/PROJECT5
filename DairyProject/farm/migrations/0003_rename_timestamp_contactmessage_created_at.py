# Generated by Django 4.2.5 on 2023-11-27 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_contactmessage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactmessage',
            old_name='timestamp',
            new_name='created_at',
        ),
    ]
