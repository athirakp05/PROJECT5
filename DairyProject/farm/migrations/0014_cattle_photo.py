# Generated by Django 4.2.5 on 2023-11-08 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0013_alter_seller_farmer_license'),
    ]

    operations = [
        migrations.AddField(
            model_name='cattle',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='cattle_photos/'),
        ),
    ]