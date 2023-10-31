# Generated by Django 4.2.6 on 2023-10-27 16:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CSSAPP', '0001_initial'),
        ('EtudiantApp', '0003_alter_etudiant_civilite_alter_etudiant_cycle'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='annee_academique',
            field=models.CharField(default=None, max_length=9),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='annee_frequentation_fin',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='confirmer_mot_de_passe',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='genre',
            field=models.CharField(choices=[('Homme', 'Homme'), ('Femme', 'Femme')], default='Homme', max_length=10),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='imagesprofiles',
            field=models.ImageField(default='../static/assets_dash/r.jpg', max_length=500, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='mois_debut_annee_academique',
            field=models.IntegerField(choices=[(1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')], default=9),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='mot_de_passe',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='etudiant',
            name='statut',
            field=models.CharField(choices=[('En Frequentation', 'En Fréquentation'), ('Ancien etudiant', 'Ancien étudiant')], default='En Frequentation', max_length=20),
        ),
        migrations.CreateModel(
            name='Memoire',
            fields=[
                ('Id_mem', models.AutoField(primary_key=True, serialize=False)),
                ('titre', models.CharField(max_length=255)),
                ('date_poste', models.DateField(default=datetime.date.today)),
                ('identite', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='EtudiantApp.etudiant')),
            ],
        ),
        migrations.CreateModel(
            name='Demande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet_demande', models.CharField(choices=[('attestation_frequentation', 'Attestation de fréquentation'), ('attestation_reussite', 'Attestation de réussite'), ('releve', 'Relevé')], max_length=50)),
                ('session', models.CharField(choices=[('S1', 'S1'), ('S2', 'S2'), ('S3', 'S3'), ('S4', 'S4')], max_length=2)),
                ('filiere', models.CharField(choices=[('informatique', 'Informatique'), ('administration', 'Administration')], max_length=50)),
                ('cycle', models.CharField(choices=[('DUT', 'DUT'), ('LICENCE', 'Licence')], max_length=50)),
                ('annee_academique', models.CharField(max_length=10)),
                ('identite_concerne', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='EtudiantApp.etudiant')),
                ('identite_receptioniste', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='CSSAPP.css')),
            ],
        ),
    ]