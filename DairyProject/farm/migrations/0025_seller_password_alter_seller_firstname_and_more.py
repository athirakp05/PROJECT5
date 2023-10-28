# Generated by Django 4.2.5 on 2023-10-27 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0024_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='password',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seller',
            name='firstname',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='seller',
            name='lastname',
            field=models.CharField(max_length=100),
        ),
    ]
