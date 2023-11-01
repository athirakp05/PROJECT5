# Generated by Django 4.2.5 on 2023-10-30 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0004_alter_customuser_managers_remove_customuser_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('breed_id', models.AutoField(primary_key=True, serialize=False)),
                ('breed_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('age', models.IntegerField()),
                ('milk_obtained_per_day', models.IntegerField()),
                ('health_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='ifsccode',
            old_name='accno',
            new_name='acc_no',
        ),
        migrations.RemoveField(
            model_name='ifsccode',
            name='farmer',
        ),
        migrations.RemoveField(
            model_name='society',
            name='farmer',
        ),
        migrations.AddField(
            model_name='cattle',
            name='feed',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='cattle',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cattle',
            name='medicine',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='cattle',
            name='milk_obtained_per_day',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='seller',
            field=models.ForeignKey(limit_choices_to={'role': 'Seller'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CattleBreed',
        ),
    ]