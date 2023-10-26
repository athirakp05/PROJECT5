# Generated by Django 4.2.5 on 2023-10-25 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productCode', models.AutoField(primary_key=True, serialize=False)),
                ('productType', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('mfgDate', models.DateField()),
                ('expiryDate', models.DateField()),
                ('gradeLevel', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
    ]
