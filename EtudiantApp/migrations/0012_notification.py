# Generated by Django 4.2.7 on 2023-12-06 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0011_memoire_binome_notification_envoyee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('est_lue', models.BooleanField(default=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('destinataire', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='EtudiantApp.etudiant')),
            ],
            options={
                'ordering': ['-date_creation'],
            },
        ),
    ]