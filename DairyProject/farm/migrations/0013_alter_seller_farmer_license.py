# Generated by Django 4.2.5 on 2023-11-07 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0012_alter_seller_farmer_license'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='farmer_license',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
