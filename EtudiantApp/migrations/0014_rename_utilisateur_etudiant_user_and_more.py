# Generated by Django 4.2.7 on 2023-12-08 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0013_etudiant_utilisateur'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etudiant',
            old_name='utilisateur',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='etudiant',
            name='role',
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='civilite',
            field=models.CharField(choices=[('MARIÉ', 'MARIÉ'), ('VEUF(VE)', 'VEUF(VE)'), ('Célibataire', 'Célibataire')], default='Célibataire', max_length=20),
        ),
        migrations.AlterField(
            model_name='etudiant',
            name='imagesprofiles',
            field=models.ImageField(default='images/r.jpeg', max_length=500, upload_to='images/'),
        ),
    ]
