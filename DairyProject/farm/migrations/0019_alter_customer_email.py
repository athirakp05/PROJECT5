# Generated by Django 4.2.5 on 2023-10-25 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0018_alter_customer_email_alter_customer_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(default=' ', max_length=254, unique=True),
        ),
    ]
