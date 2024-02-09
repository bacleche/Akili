from django.db import models
from EtudiantApp.data_models.etudiant import Etudiant
from DCFISPACE.data_models.directeur import Directeur
from CSSAPP.data_models.css import CSS




class Attestation(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    types_attestation = models.CharField(max_length=500)
    date_register = models.DateField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)
    is_transfer_directeur = models.BooleanField(default=False)
    is_transfer_css = models.BooleanField(default=False)
    is_transfer_etudiant = models.BooleanField(default=False)
    file = models.ImageField(upload_to='attestations/',max_length=500) 

    def __str__(self):
        return f"Attestation de {self.etudiant.user.first_name} {self.etudiant.user.last_name}"

class Bulletin(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.DO_NOTHING)
    date_register = models.DateField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)  
    is_transfer_directeur = models.BooleanField(default=False)
    is_transfer_css = models.BooleanField(default=False)
    is_transfer_etudiant = models.BooleanField(default=False)
    file = models.ImageField(upload_to='bulletins/',max_length=500) 

    def __str__(self):
        return f"Bulletin de {self.etudiant.user.first_name} {self.etudiant.user.last_name}"
