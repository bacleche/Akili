# Generated by Django 4.2.7 on 2023-12-14 03:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0023_etudiant_first_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='first_login',
        ),
    ]
