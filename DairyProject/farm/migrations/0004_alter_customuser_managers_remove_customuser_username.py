# Generated by Django 4.2.5 on 2023-10-30 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_cattle_alter_customuser_managers_customuser_username_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
