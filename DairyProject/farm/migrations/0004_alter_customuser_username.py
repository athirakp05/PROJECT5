<<<<<<< HEAD
# Generated by Django 4.2.5 on 2023-10-27 04:14

import django.contrib.auth.validators
=======
# Generated by Django 4.2.5 on 2023-10-18 16:37

>>>>>>> f9e74704650570e670252ba5fbf9dd17e094b911
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
<<<<<<< HEAD
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
=======
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
>>>>>>> f9e74704650570e670252ba5fbf9dd17e094b911
        ),
    ]
