# Generated by Django 4.2.5 on 2024-03-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_remove_society_pin_code_society_pincode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='society',
            name='pincode',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
