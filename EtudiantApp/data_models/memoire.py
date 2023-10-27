from django.db import models
from datetime import date
from EtudiantApp.data_models.etudiant import Etudiant


class Memoire(models.Model):
    # Vos autres champs
    Id_mem = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255)
    date_poste = models.DateField(default=date.today)
    identite = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    