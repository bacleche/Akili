# Generated by Django 4.2.7 on 2024-04-30 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0018_alter_etudiant_annee_academique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='etudiant',
            name='mois_debut_annee_academique',
        ),
    ]
