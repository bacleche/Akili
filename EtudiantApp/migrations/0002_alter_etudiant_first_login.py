# Generated by Django 4.2.7 on 2023-12-29 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etudiant',
            name='first_login',
            field=models.BooleanField(default=False),
        ),
    ]
