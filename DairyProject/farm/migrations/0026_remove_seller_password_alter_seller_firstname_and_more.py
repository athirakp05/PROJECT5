# Generated by Django 4.2.5 on 2023-10-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0025_seller_password_alter_seller_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='password',
        ),
        migrations.AlterField(
            model_name='seller',
            name='firstname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='seller',
            name='lastname',
            field=models.CharField(max_length=50),
        ),
    ]
