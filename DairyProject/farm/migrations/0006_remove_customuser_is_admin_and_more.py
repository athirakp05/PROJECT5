# Generated by Django 4.2.5 on 2023-10-20 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0005_remove_customuser_username_alter_customuser_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
