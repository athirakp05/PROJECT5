# Generated by Django 4.2.5 on 2023-11-07 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0007_merge_0005_login_0006_alter_customuser_is_customer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Login',
        ),
    ]
