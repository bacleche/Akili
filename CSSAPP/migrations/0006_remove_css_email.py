# Generated by Django 4.2.7 on 2023-12-12 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CSSAPP', '0005_remove_css_nom_remove_css_prenom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='css',
            name='email',
        ),
    ]
