# Generated by Django 4.2.7 on 2024-02-10 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DCFISPACE', '0003_alter_directeur_signature'),
        ('EtudiantApp', '0009_demande_date_termine'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='destinataire_dir',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notifications_destinataire_dir', to='DCFISPACE.directeur'),
        ),
        migrations.AddField(
            model_name='notification',
            name='expediteur_dir',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='notifications_expediteur_dir', to='DCFISPACE.directeur'),
        ),
    ]
