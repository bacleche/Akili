# Generated by Django 4.2.7 on 2024-03-27 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0012_remove_demande_choix_semestre_demande_choix_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='niveau_dut_demande',
            field=models.CharField(choices=[('dut1', 'DUT1'), ('dut2', 'DUT2')], default=280324, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='demande',
            name='niveau_licence_demande',
            field=models.CharField(choices=[('licence1', 'LICENCE1'), ('licence2', 'LICENCE2'), ('licence3', 'LICENCE3')], default=28032024, max_length=50),
            preserve_default=False,
        ),
    ]
