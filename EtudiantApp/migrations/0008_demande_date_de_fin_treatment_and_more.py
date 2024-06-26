# Generated by Django 4.2.7 on 2024-01-27 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0007_demande_etat'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='date_de_fin_treatment',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='demande',
            name='date_de_mise_en_traitement',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='demande',
            name='date_refus',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
