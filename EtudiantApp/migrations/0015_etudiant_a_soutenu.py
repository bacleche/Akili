# Generated by Django 4.2.7 on 2024-04-29 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0014_alter_demande_choix_session_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='a_soutenu',
            field=models.BooleanField(default=False),
        ),
    ]
