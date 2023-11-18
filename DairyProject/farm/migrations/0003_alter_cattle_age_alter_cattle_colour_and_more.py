# Generated by Django 4.2.5 on 2023-11-18 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0002_remove_cattle_id_cattle_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cattle',
            name='Age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='Colour',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='EarTagID',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='feed',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='height',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='milk_obtained',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cattle',
            name='weight',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='contact_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='coverage_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='policy_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='premium_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='provider_name',
            field=models.CharField(choices=[('Agriculture Insurance Company of India (AIC)', 'Agriculture Insurance Company of India (AIC)'), ('National Insurance Company', 'National Insurance Company'), ('United India Insurance Company', 'United India Insurance Company'), ('HDFC ERGO', 'HDFC ERGO'), ('ICICI Lombard', 'ICICI Lombard'), ('Bajaj Allianz', 'Bajaj Allianz')], default='', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='start_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='administered_by',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='date_administered',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='dosage',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='next_due_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaccination',
            name='vaccine_name',
            field=models.CharField(choices=[('Clostridial vaccines', 'Clostridial vaccines'), ('Brucellosis vaccine', 'Brucellosis vaccine'), ('Caseous lymphadenitis (CL) vaccine', 'Caseous lymphadenitis (CL) vaccine'), ('Rinderpest vaccine', 'Rinderpest vaccine'), ('Foot and mouth disease (FMD vaccine)', 'Foot and mouth disease (FMD) vaccine')], default='', max_length=50, null=True, unique=True),
        ),
    ]
