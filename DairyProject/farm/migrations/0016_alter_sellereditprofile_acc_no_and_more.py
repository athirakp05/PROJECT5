# Generated by Django 4.2.5 on 2023-11-12 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0015_alter_sellereditprofile_pin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellereditprofile',
            name='acc_no',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='sellereditprofile',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='sellereditprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='sellereditprofile',
            name='rationcard_no',
            field=models.IntegerField(null=True),
        ),
    ]
