# Generated by Django 4.2.5 on 2024-04-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_alter_milksample_color_alter_milksample_fat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
