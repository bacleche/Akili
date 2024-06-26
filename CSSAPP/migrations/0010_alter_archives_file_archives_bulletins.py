# Generated by Django 4.2.7 on 2024-03-03 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EtudiantApp', '0010_notification_destinataire_dir_and_more'),
        ('CSSAPP', '0009_alter_attestation_file_alter_bulletin_file_archives'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archives',
            name='file',
            field=models.FileField(max_length=500, upload_to='archives/'),
        ),
        migrations.CreateModel(
            name='Archives_bulletins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_archivage', models.DateField(auto_now_add=True)),
                ('file', models.FileField(max_length=500, upload_to='archives-bulletins/')),
                ('is_archived', models.BooleanField(default=False)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='EtudiantApp.etudiant')),
            ],
        ),
    ]
