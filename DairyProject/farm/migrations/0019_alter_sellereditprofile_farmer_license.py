# Generated by Django 4.2.5 on 2023-11-12 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0018_alter_sellereditprofile_society'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellereditprofile',
            name='farmer_license',
            field=models.CharField(max_length=50),
        ),
    ]
