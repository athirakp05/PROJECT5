# Generated by Django 4.2.5 on 2024-02-28 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_meeting_id_meeting_meeting_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
