# Generated by Django 4.2.7 on 2024-01-27 15:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0008_demande_date_de_fin_treatment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='date_termine',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
